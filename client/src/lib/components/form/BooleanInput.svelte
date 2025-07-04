<script>

let {input, error, errors, value= $bindable(), label="", name, forName="", autocomplete="", required=false, choices=[], constraints=[], type="text", css="", form=undefined, step=1} = $props();
const inputProperties = { type };

let requiredClass = required ? "required" : ""; 
let hasErrors = errors && errors[name];
let classes = hasErrors ? "with-error" : "";
let errorClass = hasErrors ? "preset-outlined-error-500" : "";

let baseClassLookup = {
    textarea: "textarea",
    file: "",
    select: "select",
    input: "input"
}

let baseClass = baseClassLookup[type] || "input";

</script>
<input
{name}
style="{css}"
class="{baseClass} {errorClass}"
type="checkbox"
bind:checked={value}/>
