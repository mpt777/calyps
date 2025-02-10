import { postRecipe } from "$scripts/actions/recipe";
import { recipeSchema } from "$lib/forms/recipe";
import { addMessage, Message } from "$scripts/message";
import { papi } from "$utils/api";
import { toJson } from "$utils/form";
import { url } from "$utils/url.js";
import { fail, redirect } from "@sveltejs/kit";

import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { z } from 'zod';
import { safeJson } from "$scripts/permissions/permissions";
import { getDefaults } from "$scripts/validation";

export async function load({ fetch }) {
    // const form = await superValidate(zod(recipeSchema));
    
    const form = getDefaults(recipeSchema);
    console.log("HELLO", form)
    const units = await safeJson(await papi(fetch, "recipe/unit/"));
    const visbilities = await safeJson(await papi(fetch, "common/visibility/"));

    return { form:form, message:"", units, visbilities};
}

export const actions = {
    default: async(event) => {
        let response = await postRecipe(event);
        return response
    }
}
