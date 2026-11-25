"""Turn lines of OCR text from a recipe card into a ``RecipeDraft``.

This is engine-agnostic: any extractor that produces plain text lines in
reading order (top to bottom) can reuse it. It is heuristic: it looks for
section headers ("Ingredients", "Directions"), quantities at the start of a
line, numbered steps, and "Serves 4" / "Prep: 15 min" style metadata. The
result is a draft for a person to review, not a finished recipe.
"""
import re
from fractions import Fraction
from typing import Iterable, Optional

from .base import IngredientDraft, RecipeDraft

UNICODE_FRACTIONS = {
    "½": "1/2", "⅓": "1/3", "⅔": "2/3", "¼": "1/4", "¾": "3/4",
    "⅕": "1/5", "⅖": "2/5", "⅗": "3/5", "⅘": "4/5", "⅙": "1/6",
    "⅚": "5/6", "⅛": "1/8", "⅜": "3/8", "⅝": "5/8", "⅞": "7/8",
}

# Spellings seen on cards -> Unit.code in the database. Matched
# case-insensitively, except the single letters "t" / "T" (handled separately),
# where case is the only thing telling teaspoon from tablespoon.
UNIT_ALIASES = {
    "cup": ["cups", "cup", "c"],
    "tsp": ["teaspoons", "teaspoon", "tsps", "tsp", "tspn", "ts"],
    "tbsp": ["tablespoons", "tablespoon", "tbsps", "tbsp", "tbls", "tbl", "tbs", "tb"],
    "pt": ["pints", "pint", "pts", "pt"],
    "qt": ["quarts", "quart", "qts", "qt"],
    "gal": ["gallons", "gallon", "gal"],
    "fl oz": ["fluid ounces", "fluid ounce", "fl. oz", "fl oz", "floz"],
    "oz": ["ounces", "ounce", "oz"],
    "lb": ["pounds", "pound", "lbs", "lb", "#"],
    "ml": ["milliliters", "millilitres", "milliliter", "millilitre", "ml"],
    "l": ["liters", "litres", "liter", "litre", "l"],
    "g": ["grams", "gram", "gr", "g"],
    "kg": ["kilograms", "kilogram", "kgs", "kg"],
}

NUMBER = r"\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?"
QUANTITY_RE = re.compile(
    rf"^(?P<amount>{NUMBER})(?:\s*(?:-|–|to)\s*(?:{NUMBER}))?\s*(?P<rest>.*)$"
)
STEP_NUMBER_RE = re.compile(r"^(?:step\s*)?(\d{1,2})\s*[.):\-]\s+", re.IGNORECASE)
BULLET_RE = re.compile(r"^[-•*·o]\s+")

INGREDIENT_HEADER_RE = re.compile(
    r"^(?:ingredients?|you(?:'ll| will)? need|what you need)\s*[:\-]?\s*(?P<rest>.*)$",
    re.IGNORECASE,
)
STEP_HEADER_RE = re.compile(
    r"^(?:directions?|instructions?|method|steps?|preparation|procedure|how to make)"
    r"\s*[:\-]?\s*(?P<rest>.*)$",
    re.IGNORECASE,
)

DURATION_RE = (
    r"(?:(?P<h>\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hour|hours)\b\.?)?\s*"
    r"(?:(?P<m>\d+)\s*(?:m|min|mins|minute|minutes)\b\.?)?"
)
PREP_RE = re.compile(rf"\bprep(?:aration)?(?:\s*time)?\s*[:\-]?\s*{DURATION_RE}", re.IGNORECASE)
COOK_RE = re.compile(
    rf"\b(?:cook|cooking|bake|baking|roast|grill)(?:\s*time)?\s*[:\-]?\s*(?:for\s*)?{DURATION_RE}",
    re.IGNORECASE,
)
# For steps like "Bake in a greased pan for 25 minutes", when the card has no
# explicit cook time.
STEP_COOK_RE = re.compile(
    rf"\b(?:cook|bake|roast|grill|simmer|fry|boil)\b[^.]*?\bfor\s+(?:about\s+)?{DURATION_RE}",
    re.IGNORECASE,
)
SERVINGS_RE = re.compile(
    r"\b(?:serves|servings?|yields?|makes)\s*[:\-]?\s*(?:about\s*)?(?P<n>\d+)"
    r"|(?P<n2>\d+)\s*(?:servings|portions)\b",
    re.IGNORECASE,
)
METADATA_ONLY_RE = re.compile(
    r"^(?:(?:prep|cook|bake|total|active)\w*(?:\s*time)?|serves|servings?|yields?|makes)\b",
    re.IGNORECASE,
)


def parse_recipe_lines(lines: Iterable[str], unit_codes: Iterable[str]) -> RecipeDraft:
    lines = [normalize_line(line) for line in lines]
    lines = [line for line in lines if line]
    unit_lookup = build_unit_lookup(unit_codes)

    draft = RecipeDraft(raw_text="\n".join(lines))
    description: list[str] = []
    section = "intro"  # intro -> ingredients -> steps
    # True once an "Ingredients" header is seen. Without one, a line only
    # counts as an ingredient if it starts with a quantity.
    labelled_ingredients = False

    for line in lines:
        if parse_metadata(line, draft) and METADATA_ONLY_RE.match(line):
            continue

        header = INGREDIENT_HEADER_RE.match(line)
        if header:
            section = "ingredients"
            labelled_ingredients = True
            line = header.group("rest")
            if not line:
                continue
        else:
            header = STEP_HEADER_RE.match(line)
            if header:
                section = "steps"
                line = header.group("rest")
                if not line:
                    continue

        if not draft.name and section == "intro" and not looks_like_ingredient(line):
            draft.name = line.strip(" :-")
            continue

        if section == "steps" or STEP_NUMBER_RE.match(line):
            if section != "steps" and draft.ingredients:
                section = "steps"
            add_step(draft.instructions, line)
            continue

        in_ingredient_list = section == "ingredients" and labelled_ingredients and not looks_like_sentence(line)
        if in_ingredient_list or looks_like_ingredient(line):
            if section == "intro":
                section = "ingredients"
            add_ingredient(draft.ingredients, line, unit_lookup)
            continue

        # Unlabelled prose: before the ingredients it describes the dish,
        # after them it's almost always the method.
        if draft.ingredients:
            section = "steps"
            add_step(draft.instructions, line)
        else:
            description.append(line)

    draft.description = " ".join(description)

    if draft.cook_time is None:
        for step in draft.instructions:
            seconds = match_duration(STEP_COOK_RE, step)
            if seconds:
                draft.cook_time = seconds
                break

    return draft


def normalize_line(line: str) -> str:
    line = line.replace("⁄", "/")  # fraction slash
    for char, ascii_fraction in UNICODE_FRACTIONS.items():
        # "1½" -> "1 1/2", "½" -> "1/2"
        line = re.sub(rf"(\d){char}", rf"\1 {ascii_fraction}", line)
        line = line.replace(char, ascii_fraction)
    return re.sub(r"\s+", " ", line).strip()


def build_unit_lookup(unit_codes: Iterable[str]) -> list[tuple[re.Pattern, str]]:
    """Patterns for the units that exist in the database, longest first."""
    known = set(unit_codes)
    patterns = []
    for code, aliases in UNIT_ALIASES.items():
        if code not in known:
            continue
        for alias in aliases:
            pattern = re.compile(rf"^{re.escape(alias)}(?:\.|\b|(?=\s)|$)\s*(?:of\s+)?", re.IGNORECASE)
            patterns.append((len(alias), pattern, code))
    # Single-letter t/T: lowercase is teaspoon, uppercase tablespoon.
    if "tsp" in known:
        patterns.append((1, re.compile(r"^t\.?(?=\s)\s*"), "tsp"))
    if "tbsp" in known:
        patterns.append((1, re.compile(r"^T\.?(?=\s)\s*"), "tbsp"))
    patterns.sort(key=lambda item: -item[0])
    return [(pattern, code) for _, pattern, code in patterns]


def looks_like_ingredient(line: str) -> bool:
    return bool(QUANTITY_RE.match(BULLET_RE.sub("", line))) and not STEP_NUMBER_RE.match(line)


def looks_like_sentence(line: str) -> bool:
    """A full sentence in the ingredient list is almost always the method starting."""
    return len(line.split()) >= 6 and line.endswith((".", "!"))


def add_ingredient(ingredients: list[IngredientDraft], line: str, unit_lookup) -> None:
    raw = line
    line = BULLET_RE.sub("", line)
    match = QUANTITY_RE.match(line)

    if not match:
        # OCR splits long handwritten lines: "1 cup butter," / "softened".
        if ingredients and ingredients[-1].raw.endswith((",", "-", "(")):
            ingredients[-1].name = f"{ingredients[-1].name} {line}".strip()
            ingredients[-1].raw = f"{ingredients[-1].raw} {raw}".strip()
            return
        ingredients.append(IngredientDraft(name=line, raw=raw))
        return

    amount = parse_number(match.group("amount"))
    rest = match.group("rest")
    unit_code = None
    for pattern, code in unit_lookup:
        unit_match = pattern.match(rest)
        if unit_match:
            unit_code = code
            rest = rest[unit_match.end():]
            break

    name = rest.strip(" ,.-") or raw
    ingredients.append(IngredientDraft(name=name, amount=amount, unit_code=unit_code, raw=raw))


def add_step(steps: list[str], line: str) -> None:
    numbered = STEP_NUMBER_RE.match(line)
    text = BULLET_RE.sub("", line[numbered.end():] if numbered else line).strip()
    if not text:
        return
    # OCR splits one handwritten sentence over several lines: keep appending
    # until a new number starts or the previous step ended its sentence.
    if steps and not numbered and not steps[-1].endswith((".", "!", "?", ":")):
        steps[-1] = f"{steps[-1]} {text}"
    else:
        steps.append(text)


def parse_metadata(line: str, draft: RecipeDraft) -> bool:
    found = False
    servings = SERVINGS_RE.search(line)
    if servings and draft.servings is None:
        draft.servings = int(servings.group("n") or servings.group("n2"))
        found = True
    prep = match_duration(PREP_RE, line)
    if prep and draft.prep_time is None:
        draft.prep_time = prep
        found = True
    if METADATA_ONLY_RE.match(line):
        cook = match_duration(COOK_RE, line)
        if cook and draft.cook_time is None:
            draft.cook_time = cook
            found = True
    return found


def match_duration(pattern: re.Pattern, text: str) -> Optional[int]:
    for match in pattern.finditer(text):
        hours, minutes = match.group("h"), match.group("m")
        if hours or minutes:
            return int(float(hours or 0) * 3600 + int(minutes or 0) * 60)
    return None


def parse_number(text: str) -> Optional[float]:
    try:
        return float(sum(Fraction(part) for part in text.split()))
    except (ValueError, ZeroDivisionError):
        return None
