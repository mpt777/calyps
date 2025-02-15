import { papi } from "$utils/api";

export async function load({ params, fetch, url }) {
    const paginator = await(await papi(fetch, `recipe/search/recipe/?${url.searchParams.toString()}`, {method: "GET"})).json();
    console.log(paginator)

    return { paginator };
}