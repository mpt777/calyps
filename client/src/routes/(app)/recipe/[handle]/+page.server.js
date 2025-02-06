import { iapi } from "$utils/api";

export async function load({ params }) {
  let recipe;
  try {
      const response = await iapi(`recipe/recipe/${params.handle}`); // Make an API request
      recipe = await response.json();
  } catch (error) {
      console.error('API request failed:', error);
  }

  console.log(recipe)

  let breadcrumbs = [
      {"link":"/", "label": "Home"},
      {"link":"/", "label": recipe.title},
  ]

  return {
      recipe,
      breadcrumbs
  };
}

export const actions = {
    default: async(event) => {
      console.log("here")
        return event
    }
}