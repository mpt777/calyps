import { error, fail } from "@sveltejs/kit";

export async function safeJson(request) {
  if (request.status == 401) {
    throw error(400, {message: "Please Login and Check Permissions", level:"error"});
  }
  return await request.json();
}