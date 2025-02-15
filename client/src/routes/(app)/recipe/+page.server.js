import { papi } from "$utils/api";

export async function load({ params, fetch, url }) {
    let searchQuery = ""
    let search = url.searchParams.get('search');
    if (search) {
        searchQuery = `?search=${search}`
    }

    const recipes = await(await papi(fetch, `recipe/search/recipe/${searchQuery}`, {method: "GET"})).json();

    return { recipes };
}