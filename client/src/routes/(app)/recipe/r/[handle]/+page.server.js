import { iapi } from "$utils/api";
import { fail, error } from "@sveltejs/kit";

export async function load({ params }) {
    let recipe;

    const response = await iapi(`recipe/recipe/${params.handle}`); // Make an API request

    if (!response.ok) {
        throw error(response.status, response.statusText)
    }
    console.log(response)
    recipe = await response.json();


  let breadcrumbs = [
      {"link":"/", "label": "Home"},
      {"link":"/", "label": recipe.title},
  ]

  return {
      recipe,
      breadcrumbs
  };
}