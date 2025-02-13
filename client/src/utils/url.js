import { resolveRoute } from "$app/paths";

export const _url = {
  "login":"/login",
  "logout":"/logout",
  "signup":"/signup",
  "projects":"/projects",
  "profile":"/profile",

  "recipe": "/recipe/r/[handle]",
  "recipe_add": "/recipe/r/add",
  "recipe_edit": "/recipe/r/[handle]/edit",
}

/**
 * @param {string} alias
 */
export function url(alias, kwargs ={}) {
  console.log(alias, kwargs)
  return resolveRoute(_url[alias], kwargs)
}
