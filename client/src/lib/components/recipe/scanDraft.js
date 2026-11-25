import { generateHandle } from "$scripts/humanize";

/**
 * @typedef {{ name: string, amount: number | null, unit_code: string | null, unit: number | null, raw: string }} IngredientDraft
 * @typedef {{
 *   name: string, servings: number | null, prep_time: number | null, cook_time: number | null,
 *   description: string, instructions: string[], ingredients: IngredientDraft[], raw_text: string
 * }} RecipeDraft
 */

/** @param {string} text */
function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

/**
 * Turn a draft from POST /recipe/scan/recipe/ into the recipe form's values.
 * `defaults` supplies everything the card can't (visibility, tags, ...).
 * @param {RecipeDraft} draft
 * @param {Record<string, any>} defaults
 * @param {{ id: number }[]} units
 */
export function draftToForm(draft, defaults, units) {
  const fallbackUnit = units[0]?.id;

  const ingredients = draft.ingredients.map((ingredient, i) => ({
    name: ingredient.name,
    // The form needs a positive amount and a unit; "salt to taste" has neither.
    amount: ingredient.amount && ingredient.amount > 0 ? ingredient.amount : 1,
    unit: ingredient.unit ?? fallbackUnit,
    sequence: i + 1,
    DELETE: false,
  }));

  // Quill's ordered-list markup, so the steps open as a numbered list.
  const instructions = draft.instructions.length
    ? `<ol>${draft.instructions.map((step) => `<li data-list="ordered">${escapeHtml(step)}</li>`).join("")}</ol>`
    : "";

  return {
    ...structuredClone(defaults),
    name: draft.name || defaults.name || "",
    handle: generateHandle(draft.name || ""),
    servings: draft.servings || defaults.servings || 1,
    prep_time: draft.prep_time ?? defaults.prep_time ?? 0,
    cook_time: draft.cook_time ?? defaults.cook_time ?? 0,
    description: draft.description ? `<p>${escapeHtml(draft.description)}</p>` : "",
    instructions,
    ingredients,
  };
}

/**
 * How many draft ingredients came back without a recognised unit.
 * @param {RecipeDraft} draft
 */
export function ingredientsMissingUnit(draft) {
  return draft.ingredients.filter((ingredient) => ingredient.unit == null).length;
}
