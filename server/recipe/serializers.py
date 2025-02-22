from rest_framework import serializers

from common.serializers import GenericTagSerializer, VisibilitySerializer
from common.models import Tag, TagType, Visibility

from .models import Recipe, Ingredient, Unit
from django.contrib.auth.models import User


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name", "code", "system", "kind"]


class IngredientSerializer(serializers.ModelSerializer):
    unit_code = serializers.SlugRelatedField(read_only=True, slug_field='code', source='unit')  # Returns the unit as a string

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "recipe"]

class IngredientInlineSerializer(IngredientSerializer):
    DELETE = serializers.BooleanField(default=False)

    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "unit", "unit_code","sequence", "DELETE"]
        # extra_kwargs = {
        #     '_id': {'write_only': True},
        # }

# class TagInlineSerializer(serializers.ModelSerializer):
#     tag_type_name = serializers.CharField(write_only=True)

#     class Meta:
#         model = Tag
#         fields = ['tag_type_name']

#     def create(self, validated_data):
#         tag_type_name = validated_data.pop('tag_type_name')
#         tag_type, _ = TagType.objects.get_or_create(name=tag_type_name)
#         tag = Tag.objects.create(tag_type=tag_type, **validated_data)
#         return tag


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInlineSerializer(many=True, required=False, allow_empty=True)
    # tags = TagInlineSerializer(many=True, required=False, allow_empty=True)
    image = serializers.StringRelatedField()  # Returns image as a string
    created_by = serializers.StringRelatedField()  # Returns username of creator
    tag_types = serializers.ListSerializer(
        child=serializers.CharField(), write_only=True
    )

    def get_visibility_choices(self, obj):
        return VisibilitySerializer(Visibility.objects.all(), many=True).data
    
    def get_unit_choices(self, obj):
        return UnitSerializer(Unit.objects.all(), many=True).data

    def to_representation(self, instance):
        """Customize output to return tag type names instead of IDs."""
        data = super().to_representation(instance)
        data["tag_types"] = list(instance.tags.values_list("tag_type__name", flat=True).distinct())
        return data

    class Meta:
        model = Recipe
        fields = [
            "id", "name", "handle", "description", "instructions",
            "image", "created_by", "prep_time", "cook_time",
            "servings", "visibility", "ingredients",
            "tag_types",
            # "visibility_choices", "unit_choices"
        ]

    def _process_related(self, instance, ingredients_data):
      for ingredient_data in ingredients_data:
        DELETE = ingredient_data.pop("DELETE", False)
        ID = ingredient_data.pop("id", None)

        if DELETE:
            if ID:
                Ingredient.objects.filter(id=ID).delete()
                continue
            continue
        if ID:
            ingredient = Ingredient.objects.get(id=ID)
            for attr, value in ingredient_data.items():
                setattr(ingredient, attr, value)
                ingredient.save()
        else:
            ingredient_data["recipe"] = instance
            ingredient = Ingredient.objects.create(**ingredient_data)
            instance.ingredients.add(ingredient)
            
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        validated_data["created_by"] = User.objects.get(id=1)
        recipe = Recipe.objects.create(**validated_data)
        self._process_related(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        tag_types = validated_data.pop("tag_types", [])
        ingredients_data = validated_data.pop('ingredients', [])

        for i in range(len(ingredients_data)):
            ingredients_data[i]["id"] = self.initial_data["ingredients"][i].get("id", "")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        tag_serializer = GenericTagSerializer(data={"tag_types": tag_types}, context={"content_object": instance})
        tag_serializer.is_valid(raise_exception=True)
        tag_serializer.save()

        self._process_related(instance, ingredients_data)
        return instance
