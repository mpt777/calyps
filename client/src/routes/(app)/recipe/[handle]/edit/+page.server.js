import { postRecipe } from "$scripts/actions/recipe";
import { recipeSchema } from "$lib/forms/recipe";
import { papi } from "$utils/api";
import { toJson } from "$utils/form";
import { url } from "$utils/url";
import { fail, redirect } from "@sveltejs/kit";

import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { z } from 'zod';

export async function load({ params, fetch }) {
    const recipe = await(await papi(fetch, `recipe/recipe/${params.handle}`, {method: "GET"})).json();
    // const form = await superValidate(recipe, zod(recipeSchema));
    const form = recipeSchema.parse(recipe);
    const units = await(await papi(fetch, "recipe/unit/")).json();
    const visbilities = await(await papi(fetch, "common/visibility/")).json();

    // console.log(recipe, form)

    return { recipe, form, message:"", units, visbilities};
}

export const actions = {
    default: async(event) => {
        return await postRecipe(event);
    }
}