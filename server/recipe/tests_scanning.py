from unittest import mock

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings
from rest_framework.test import APIClient

from recipe.models import Unit
from recipe.scanning import RecipeDraft, RecipeExtractor, get_extractor
from recipe.scanning.base import IngredientDraft
from recipe.scanning.parser import parse_recipe_lines

UNIT_CODES = ["cup", "tsp", "tbsp", "pt", "qt", "gal", "oz", "fl oz", "lb", "ml", "l", "g", "kg"]


class ParseRecipeLinesTests(SimpleTestCase):
    def parse(self, text):
        return parse_recipe_lines(text.strip().splitlines(), UNIT_CODES)

    def test_card_with_headers(self):
        draft = self.parse("""
            Grandma's Snickerdoodles
            Makes 24   Prep: 15 min   Bake: 10 min
            Ingredients
            2 3/4 cups flour
            1½ cups sugar
            2 tsp cream of tartar
            1 t. baking soda
            2 T cinnamon
            1 cup butter, softened
            2 eggs
            pinch of salt
            Directions
            1. Cream butter and sugar,
            then beat in the eggs.
            2. Roll into balls and coat in cinnamon sugar.
            3. Bake at 400 for 10 minutes.
        """)
        self.assertEqual(draft.name, "Grandma's Snickerdoodles")
        self.assertEqual(draft.servings, 24)
        self.assertEqual(draft.prep_time, 15 * 60)
        self.assertEqual(draft.cook_time, 10 * 60)

        parsed = [(i.amount, i.unit_code, i.name) for i in draft.ingredients]
        self.assertEqual(parsed, [
            (2.75, "cup", "flour"),
            (1.5, "cup", "sugar"),
            (2.0, "tsp", "cream of tartar"),
            (1.0, "tsp", "baking soda"),
            (2.0, "tbsp", "cinnamon"),
            (1.0, "cup", "butter, softened"),
            (2.0, None, "eggs"),
            (None, None, "pinch of salt"),
        ])
        self.assertEqual(draft.instructions, [
            "Cream butter and sugar, then beat in the eggs.",
            "Roll into balls and coat in cinnamon sugar.",
            "Bake at 400 for 10 minutes.",
        ])

    def test_card_without_headers(self):
        draft = self.parse("""
            Quick Pancakes
            Fluffy weekend pancakes
            1 cup milk
            250g flour
            2 tbsp melted butter
            Whisk everything together until smooth.
            Cook on a hot griddle for 2 min per side.
        """)
        self.assertEqual(draft.name, "Quick Pancakes")
        self.assertEqual(draft.description, "Fluffy weekend pancakes")
        self.assertEqual([(i.amount, i.unit_code) for i in draft.ingredients], [
            (1.0, "cup"), (250.0, "g"), (2.0, "tbsp"),
        ])
        self.assertEqual(len(draft.instructions), 2)
        # No "Cook time" line, so it falls back to the time in the steps.
        self.assertEqual(draft.cook_time, 2 * 60)

    def test_units_not_in_database_are_left_blank(self):
        draft = parse_recipe_lines(["Soup", "Ingredients", "2 cups stock"], ["tsp"])
        self.assertEqual(draft.ingredients[0].unit_code, None)
        self.assertEqual(draft.ingredients[0].name, "cups stock")

    def test_word_starting_with_unit_letter_is_not_a_unit(self):
        draft = self.parse("Ingredients\n2 large eggs\n3 garlic cloves\n1 chopped onion")
        self.assertEqual([i.unit_code for i in draft.ingredients], [None, None, None])
        self.assertEqual([i.name for i in draft.ingredients], ["large eggs", "garlic cloves", "chopped onion"])

    def test_medium_is_not_minutes(self):
        draft = self.parse("Stew\nIngredients\n2 lb beef\nDirections\nCook 2 medium onions until soft.")
        self.assertIsNone(draft.cook_time)

    def test_hours_and_minutes(self):
        draft = self.parse("Roast\nCook time: 1 hr 30 min")
        self.assertEqual(draft.cook_time, 90 * 60)

    def test_empty_input(self):
        self.assertEqual(parse_recipe_lines([], UNIT_CODES).to_dict(), RecipeDraft().to_dict())


class FakeExtractor(RecipeExtractor):
    def __init__(self, **options):
        self.options = options

    def extract(self, image_bytes, unit_codes):
        return RecipeDraft(
            name="Fake",
            ingredients=[
                IngredientDraft(name="flour", amount=2, unit_code="cup"),
                IngredientDraft(name="eggs", amount=2, unit_code=None),
            ],
        )


@override_settings(
    RECIPE_SCAN_EXTRACTOR="recipe.tests_scanning.FakeExtractor",
    RECIPE_SCAN_OPTIONS={"flavour": "test"},
)
class RecipeScanViewTests(TestCase):
    url = "/api/v1/recipe/scan/recipe/"

    def setUp(self):
        get_extractor.cache_clear()
        self.addCleanup(get_extractor.cache_clear)
        self.cup = Unit.objects.get_or_create(code="cup", defaults={"name": "cup", "system": 0, "kind": 0})[0]
        self.client = APIClient()
        self.client.force_authenticate(User.objects.create_user("cook", password="x"))

    def image(self, content_type="image/jpeg"):
        return SimpleUploadedFile("card.jpg", b"not really a jpeg", content_type=content_type)

    def test_returns_draft_with_unit_ids(self):
        response = self.client.post(self.url, {"image": self.image()}, format="multipart")
        self.assertEqual(response.status_code, 200)
        draft = response.json()["draft"]
        self.assertEqual(draft["name"], "Fake")
        self.assertEqual(draft["ingredients"][0]["unit"], self.cup.id)
        self.assertIsNone(draft["ingredients"][1]["unit"])

    def test_extractor_is_configurable(self):
        self.assertIsInstance(get_extractor(), FakeExtractor)
        self.assertEqual(get_extractor().options, {"flavour": "test"})

    def test_requires_login(self):
        response = APIClient().post(self.url, {"image": self.image()}, format="multipart")
        self.assertIn(response.status_code, (401, 403))

    def test_rejects_missing_and_non_image_files(self):
        self.assertEqual(self.client.post(self.url, {}, format="multipart").status_code, 400)
        response = self.client.post(self.url, {"image": self.image("text/plain")}, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_engine_failure_is_a_clean_error(self):
        with mock.patch.object(FakeExtractor, "extract", side_effect=RuntimeError("boom")):
            response = self.client.post(self.url, {"image": self.image()}, format="multipart")
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("boom", response.content.decode())


class GluedQuantityTests(SimpleTestCase):
    def test_quantity_touching_the_name(self):
        # EasyOCR sometimes drops the space: "1egg, beaten".
        draft = parse_recipe_lines(["Ingredients", "1egg, beaten", "2cups milk"], UNIT_CODES)
        self.assertEqual([(i.amount, i.unit_code, i.name) for i in draft.ingredients], [
            (1.0, None, "egg, beaten"),
            (2.0, "cup", "milk"),
        ])
