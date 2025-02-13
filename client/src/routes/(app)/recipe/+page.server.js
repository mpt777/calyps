import { papi } from "$utils/api";

export async function load({ params, fetch }) {
    const recipes = await(await papi(fetch, `recipe/search/recipe/`, {method: "GET"})).json();

    return { recipes };
}