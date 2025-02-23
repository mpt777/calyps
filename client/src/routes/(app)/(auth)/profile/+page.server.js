import { loginUser } from "$scripts/auth";
import { addMessage, Message } from "$scripts/message";
import { papi } from "$utils/api";
import { redirect } from "@sveltejs/kit";

export async function load({ locals, fetch, cookies }) {
  if (!locals.user) {
    addMessage(cookies, new Message({message: "Please Login"}));
    throw redirect(307, "/login")
  }
  
  const paginator = await(await papi(fetch, `recipe/me/recipe/`, {method: "GET"})).json();
  const profile = await(await papi(fetch, `auth/profile/`, {method: "GET"})).json();

  return { paginator, profile};
}

export const actions = {
    default: async(event) => {
        return await loginUser(event)
        //throw redirect(303, "/");
    }
}