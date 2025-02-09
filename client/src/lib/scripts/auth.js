import { fail, redirect } from "@sveltejs/kit";
import { deleteAuthToken, deleteUser, setAuthToken, setUser } from "$utils/auth";
import { addMessage, Message } from "$scripts/message";
import { papi } from "$utils/api"
import { toJson } from "$utils/form";

function tokenError(event, responseData) {
    if (responseData?.code == "token_not_valid") {
        addMessage(event.cookies, new Message({message: "Auth Error. We logged you out. Please login again"}));
        logoutUser(event)
        throw redirect(303, "/login")
    }
}

export async function loginUser(event){
    const data = toJson(await event.request.formData());

    const response = await papi(event.fetch, "auth/login", {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(data)
    });
    
    // let body = await response.text()
    // console.log(body)
    // return fail(400, {message: body, level:"error"})
    // console.log(await response.text())
    // console.log(response)
    let responseData = await response.json()

    tokenError(event, responseData);

    if (response.ok){
        setAuthToken(event.cookies, responseData.access)
        setUser(event, responseData.user)
    }
    else {
        return fail(400, {message: responseData?.message || responseData?.messages, errors: responseData?.errors, level:"error"})
    }

    const redirectTo = event.url.searchParams.get("redirectTo") || "/";
    if (redirectTo) {
        addMessage(event.cookies, new Message({message: "Success in logging in!"}));
        throw redirect(302,`/${redirectTo.slice(1)}`)
    }
    return {success: true, message: responseData.message, level:"success"};
}

export async function signupUser(event) {
    const data = toJson(await event.request.formData());

    const response = await papi(event.fetch, "auth/signup", {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(data)
    });


    let responseData = await response.json()

    tokenError(event, responseData);


    if (response.ok){
        setAuthToken(event.cookies, responseData.access)
        setUser(event, responseData.user)
    }
    else {
        return fail(400, {message: responseData?.message, errors: responseData?.errors, level:"error"})
    }

    const redirectTo = event.url.searchParams.get("redirectTo") || "/";
    if (redirectTo) {
        addMessage(event.cookies, new Message({message: "Signed Up Successfully!"}));
        throw redirect(302,`/${redirectTo.slice(1)}`)
    }

    return {success: true};
}

export function logoutUser(event) {
    deleteAuthToken(event.cookies);
    deleteUser(event)
}