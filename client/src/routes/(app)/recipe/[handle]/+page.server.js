import { iapi } from "$utils/api";

export async function load({ params }) {
  let recipe;
  try {
      const response = await iapi(`recipe/recipe/${params.handle}`); // Make an API request
      recipe = await response.json();
  } catch (error) {
      console.error('API request failed:', error);
  }


  let breadcrumbs = [
      {"link":"/", "label": "Home"},
      {"link":"/", "label": recipe.title},
  ]

  return {
      recipe,
      breadcrumbs
  };
}