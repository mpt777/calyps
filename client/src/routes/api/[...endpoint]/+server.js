import { setAuthToken } from "$utils/auth";
import { fail, redirect } from "@sveltejs/kit";

function replacePath(request, params, url) {
  return `http://server:8000/api/${params.endpoint}?${url.searchParams.toString()}`
}

export async function GET({ request, params, url, fetch}) {
  console.log(replacePath(request, params, url))
  let x = await fetch(replacePath(request, params, url));
  return x
}

export async function POST({ request, params, url, fetch}) {
  let x = await fetch(replacePath(request, params, url));
  return x
}

export async function DELETE({ request, params, url, fetch}) {
  let x = await fetch(replacePath(request, params, url));
  return x
}