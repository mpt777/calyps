"""Common types for turning a photo of a recipe card into a draft recipe.

An extractor takes raw image bytes and returns a ``RecipeDraft``. Swap the
implementation with the ``RECIPE_SCAN_EXTRACTOR`` setting; nothing else in the
app needs to know which OCR engine (or model) is behind it.
"""
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class IngredientDraft:
    name: str
    amount: Optional[float] = None
    # Unit.code as stored in the database ("cup", "tsp", ...), or None when the
    # card gave no unit or one we don't recognise.
    unit_code: Optional[str] = None
    # The line as it was read, so the user can see what the guess was based on.
    raw: str = ""


@dataclass
class RecipeDraft:
    name: str = ""
    servings: Optional[int] = None
    prep_time: Optional[int] = None  # seconds, matching Recipe.prep_time
    cook_time: Optional[int] = None  # seconds, matching Recipe.cook_time
    description: str = ""
    instructions: list[str] = field(default_factory=list)
    ingredients: list[IngredientDraft] = field(default_factory=list)
    # Everything the engine read, top to bottom, for debugging and for the user
    # to copy from when the parser guessed wrong.
    raw_text: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class RecipeExtractor(ABC):
    """Reads a recipe from an image.

    Implementations should be safe to reuse across requests: ``get_extractor``
    builds one instance per process and keeps it, so expensive setup (loading
    OCR weights, creating API clients) happens once.
    """

    @abstractmethod
    def extract(self, image_bytes: bytes, unit_codes: list[str]) -> RecipeDraft:
        """Return a draft recipe read from ``image_bytes``.

        ``unit_codes`` are the Unit codes that exist in the database; only these
        should be returned as ``IngredientDraft.unit_code``.
        """


class ExtractionError(Exception):
    """The image could not be read (not an image, unreadable, engine failure)."""
