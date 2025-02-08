import { recipeSchema } from "$lib/forms/recipe";
import { papi } from "$utils/api";
import { toJson } from "$utils/form";
import { fail } from "@sveltejs/kit";

import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { z } from 'zod';

export async function load({ fetch }) {
    const form = await superValidate(zod(recipeSchema));
    
    const units = await(await papi(fetch, "recipe/unit/")).json();
    const visbilities = await(await papi(fetch, "common/visibility/")).json();

    return { form, message:"", units, visbilities};
}

export const actions = {
    default: async(event) => {
        const form = await superValidate(event, zod(recipeSchema));

        if (!form.valid) {
            console.log("FAIL")
            return fail(400, { form, message: "Validation Failed", level:"error"});
        }

        const response = await papi(event.fetch, "recipe/recipe/", {
            method: "POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify(form.data)
        });

      let responseData = await response.json()

      if (response.ok){
        return {form}
      }
      else {
          form.errors = {...form.errors, ...responseData.errors};
          return fail(400, {form, message: responseData?.message || responseData?.messages, level:"error"})
      }

    }
}