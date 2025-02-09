import { recipeSchema } from "$lib/forms/recipe";
import { addMessage, Message } from "$scripts/message";
import { papi } from "$utils/api";
import { toJson } from "$utils/form";
import { url } from "$utils/url";
import { fail, redirect } from "@sveltejs/kit";

import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { z } from 'zod';

export async function postRecipe(event) {
  let d = await event.request.formData();
  console.log(d)
  console.log("POST", event.request.data)
  const form = recipeSchema.safeParse(event.data);

  console.log("VALID FORM", form)

  if (!form.success) {
      console.log("FAIL")
      let errors = form.error.format()
      let issues = form.error.issues
      console.log(errors, issues)
      return fail(400, { form, errors, message: "Validation Failed", level:"error"});
  }

  let handle = "";
  let METHOD = "POST";
  if (event.params.handle) {
    handle=event.params.handle + "/";
    METHOD = "PATCH"
  }

  console.log(METHOD)

  const response = await papi(event.fetch, `recipe/recipe/${handle}`, {
      method: METHOD,
      headers:{
          "Content-Type":"application/json"
      },
      body: JSON.stringify(form.data)
  });

  let responseData = await response.json()

  if (response.ok){
    addMessage(event.cookies, new Message({message: "Recipe Updated!"}));
    throw redirect(303, url("recipe_edit", {handle: responseData.recipe.handle}))
    // return {form, message: responseData?.message || responseData?.messages || responseData?.detail || "Updated", level:"success"}
  }
  else {
      form.errors = {...form.errors, ...responseData.errors};
      return fail(400, {form, message: responseData?.message || responseData?.messages || responseData?.detail, level:"error"})
  }
}