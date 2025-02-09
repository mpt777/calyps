import { recipeSchema } from "$lib/forms/recipe";
import { addMessage, Message } from "$scripts/message";
import { formatZodError } from "$scripts/validation";
import { papi } from "$utils/api";
import { toJson } from "$utils/form";
import { url } from "$utils/url";
import { fail, redirect } from "@sveltejs/kit";

import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { z } from 'zod';

export async function postRecipe(event) {
  let d = await event.request.formData();
  let data = JSON.parse(d.get("hack"))
  const form = recipeSchema.safeParse(data);

  if (!form.success) {
      let errors = formatZodError(form.error.issues)
      return fail(400, { errors, message: "Validation Failed", level:"error"});
  }

  let handle = "";
  let METHOD = "POST";
  if (event.params.handle) {
    handle=event.params.handle + "/";
    METHOD = "PATCH"
  }

  console.log(METHOD, form.data)

  const response = await papi(event.fetch, `recipe/recipe/${handle}`, {
      method: METHOD,
      headers:{
          "Content-Type":"application/json"
      },
      body: JSON.stringify(form.data)
  });

  let responseData = await response.json()
  console.log(responseData)

  if (response.ok){
    addMessage(event.cookies, new Message({message: "Recipe Updated!"}));
    throw redirect(303, url("recipe_edit", {handle: responseData.recipe.handle}))
    // return {form, message: responseData?.message || responseData?.messages || responseData?.detail || "Updated", level:"success"}
  }
  else {
      return fail(400, {errors:responseData.errors, message: responseData?.message || responseData?.messages || responseData?.detail || "Success", level:"error"})
  }
}