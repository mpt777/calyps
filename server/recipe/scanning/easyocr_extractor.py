"""EasyOCR-backed recipe extractor.

Settings (all optional), passed through ``RECIPE_SCAN_OPTIONS``:

    languages                EasyOCR language codes, default ["en"]
    gpu                      use CUDA if available, default False
    model_storage_directory  where EasyOCR keeps its weights (default: EasyOCR's own, ~/.EasyOCR/model)
    user_network_directory   EasyOCR always creates this folder (default: <model_storage_directory>/user_network)
    download_enabled         let EasyOCR download missing weights, default True
    max_image_side           downscale photos so the long side is at most this many px, default 2000
    min_confidence           drop text EasyOCR is less sure of than this (0-1), default 0.2
    readtext_options         extra keyword arguments for easyocr.Reader.readtext, merged over
                             DEFAULT_READTEXT_OPTIONS
"""
import io
import threading
from statistics import median

from .base import ExtractionError, RecipeDraft, RecipeExtractor
from .parser import parse_recipe_lines

# EasyOCR's defaults (low_text=0.4, text_threshold=0.7) often miss a lone "1"
# in front of a unit ("1 tsp vanilla" -> "tsp vanilla"). These pick it up
# without slowing reading down.
# canvas_size caps the image the text detector works on (EasyOCR's default is
# 2560): 1280 reads a card just as well and peaks ~200 MB lower.
DEFAULT_READTEXT_OPTIONS = {"low_text": 0.3, "text_threshold": 0.6, "canvas_size": 1280}


class EasyOCRExtractor(RecipeExtractor):
    def __init__(
        self,
        languages=None,
        gpu=False,
        model_storage_directory=None,
        user_network_directory=None,
        download_enabled=True,
        max_image_side=2000,
        min_confidence=0.2,
        readtext_options=None,
    ):
        # Imported here so Django starts (and other extractors work) without
        # EasyOCR/torch installed.
        import os

        import easyocr

        if model_storage_directory and not user_network_directory:
            user_network_directory = os.path.join(model_storage_directory, "user_network")

        self.reader = easyocr.Reader(
            languages or ["en"],
            gpu=gpu,
            model_storage_directory=model_storage_directory,
            user_network_directory=user_network_directory,
            download_enabled=download_enabled,
            verbose=False,
        )
        self.max_image_side = max_image_side
        self.min_confidence = min_confidence
        self.readtext_options = {**DEFAULT_READTEXT_OPTIONS, **(readtext_options or {})}
        # One reader is shared by every request in the process; torch models
        # aren't guaranteed to be safe to run from several threads at once.
        self._lock = threading.Lock()

    def extract(self, image_bytes: bytes, unit_codes: list[str]) -> RecipeDraft:
        image = self._load_image(image_bytes)
        with self._lock:
            results = self.reader.readtext(image, **self.readtext_options)
        lines = self._group_into_lines(results)
        return parse_recipe_lines(lines, unit_codes)

    def _load_image(self, image_bytes: bytes):
        import numpy as np
        from PIL import Image, ImageOps, UnidentifiedImageError

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image = ImageOps.exif_transpose(image)  # phone photos are often stored sideways
            image = image.convert("RGB")
        except (UnidentifiedImageError, OSError) as error:
            raise ExtractionError("That file isn't an image we can read.") from error

        if max(image.size) > self.max_image_side:
            image.thumbnail((self.max_image_side, self.max_image_side))
        return np.array(image)

    def _group_into_lines(self, results) -> list[str]:
        """Rebuild lines of text from EasyOCR's word/phrase boxes.

        Boxes whose vertical centres are close are one line, read left to
        right. A wide horizontal gap splits a row into separate lines, so a
        card with ingredients in two columns doesn't merge them together.
        """
        boxes = []
        for points, text, confidence in results:
            if confidence < self.min_confidence or not text.strip():
                continue
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            boxes.append({
                "text": text.strip(),
                "left": min(xs),
                "right": max(xs),
                "center_y": (min(ys) + max(ys)) / 2,
                "height": max(ys) - min(ys),
            })
        if not boxes:
            return []

        typical_height = median(box["height"] for box in boxes) or 1
        boxes.sort(key=lambda box: box["center_y"])

        rows: list[list[dict]] = []
        for box in boxes:
            if rows and abs(box["center_y"] - rows[-1][-1]["center_y"]) < typical_height * 0.5:
                rows[-1].append(box)
            else:
                rows.append([box])

        lines = []
        for row in rows:
            row.sort(key=lambda box: box["left"])
            current = [row[0]]
            for box in row[1:]:
                if box["left"] - current[-1]["right"] > typical_height * 3:
                    lines.append(" ".join(item["text"] for item in current))
                    current = [box]
                else:
                    current.append(box)
            lines.append(" ".join(item["text"] for item in current))
        return lines
