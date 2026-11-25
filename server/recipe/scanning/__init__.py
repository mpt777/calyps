from functools import lru_cache

from django.conf import settings
from django.utils.module_loading import import_string

from .base import ExtractionError, IngredientDraft, RecipeDraft, RecipeExtractor

DEFAULT_EXTRACTOR = "recipe.scanning.easyocr_extractor.EasyOCRExtractor"


@lru_cache(maxsize=1)
def get_extractor() -> RecipeExtractor:
    """Build the configured extractor once per process.

    Configure with, e.g.::

        RECIPE_SCAN_EXTRACTOR = "recipe.scanning.easyocr_extractor.EasyOCRExtractor"
        RECIPE_SCAN_OPTIONS = {"languages": ["en"], "gpu": False}

    ``RECIPE_SCAN_OPTIONS`` is passed to the extractor's constructor as keyword
    arguments, so each engine can take its own settings.
    """
    path = getattr(settings, "RECIPE_SCAN_EXTRACTOR", DEFAULT_EXTRACTOR)
    options = getattr(settings, "RECIPE_SCAN_OPTIONS", {}) or {}
    extractor_class = import_string(path)
    extractor = extractor_class(**options)
    if not isinstance(extractor, RecipeExtractor):
        raise TypeError(f"{path} must subclass recipe.scanning.base.RecipeExtractor")
    return extractor


__all__ = [
    "ExtractionError",
    "IngredientDraft",
    "RecipeDraft",
    "RecipeExtractor",
    "get_extractor",
]
