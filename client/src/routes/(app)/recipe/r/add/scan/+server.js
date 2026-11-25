import { papi } from "$utils/api";
import { json } from "@sveltejs/kit";

// Forwards a recipe-card photo to Django, which returns a draft recipe.
// `fetch` here goes through handleFetch, which adds the user's auth token.
export async function POST({ request, fetch }) {
  const incoming = await request.formData();
  const image = incoming.get("image");
  if (!(image instanceof File) || image.size === 0) {
    return json({ message: "Choose a photo of the recipe card first." }, { status: 400 });
  }

  const body = new FormData();
  body.append("image", image, image.name || "recipe-card.jpg");

  let response;
  try {
    response = await papi(fetch, "recipe/scan/recipe/", { method: "POST", body });
  } catch {
    return json({ message: "Couldn't reach the server. Try again in a moment." }, { status: 502 });
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message =
      response.status === 401 || response.status === 403
        ? "Log in to scan a recipe card."
        : data.message || "Something went wrong reading that photo.";
    return json({ message }, { status: response.status });
  }
  return json(data);
}
