import { papi } from "$utils/api";
import { toJson } from "$utils/form";
import { fail } from "@sveltejs/kit";

export async function load({ fetch }) {
}

export const actions = {
    default: async(event) => {
      const data = toJson(await event.request.formData());

      console.log(data)

      const response = await papi(event.fetch, "recipe/recipe/", {
          method: "POST",
          headers:{
              "Content-Type":"application/json"
          },
          body: JSON.stringify(data)
      });

      let responseData = await response.json()

      if (response.ok){
      }
      else {
          console.log(responseData)
          return fail(400, {message: responseData?.message || responseData?.messages, errors: responseData?.errors, level:"error"})
      }

    }
}