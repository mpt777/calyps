import type { Cookies } from "@sveltejs/kit";

interface IMessage {
    title?: string,
    message: string,
    background?: string,
    timeout?: number,
    hoverable?: boolean,
    hideDismiss?: boolean,
    classes?: string
}

export class Message implements IMessage {
    public message;
    public background;
    public timeout;
    public hoverable;
    public hideDismiss;
    public classes;
    public title;

    constructor(imessage:IMessage) {
        this.title = imessage.title || "";
        this.message = imessage.message || "";
        this.background=imessage.background || "preset-filled-secondary-500";
        this.timeout=imessage.timeout || 5000;
        this.hoverable=imessage.hoverable || false;
        this.hideDismiss=imessage.hideDismiss || false;
        this.classes=imessage.classes || "";
    }
}

let messages : Message[] = [];

export function addMessage(cookies: Cookies, message : Message) {
    console.log("Message Added")
    let messages : Message[] = [
        message,
        ...JSON.parse(cookies.get("toastMessages") || "[]")
    ]

    cookies.set('toastMessages', JSON.stringify(messages), {
        httpOnly: false,
        path: '/',
        secure: true,
        sameSite: 'strict',
        maxAge: 60 * 60 * 24 // 1 day
    });    
}

export function getAndDeleteMessages(cookies: Cookies) : Message[]  {
    // todo, does not work with the layout API
    let messages = JSON.parse(cookies.get("toastMessages") || "[]") || [];    
    // cookies.delete("toastMessages", { path: '/' });
    return messages;
}