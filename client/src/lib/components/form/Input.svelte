<script lang="ts">
    import DurationField from "./DurationField.svelte";

    
  export let value : any;
  export let placeholder = "";
  export let name = "";
  export let autocomplete = "" || null;
  export let required = false;
  export let errors = {};
  export let type = "text";
  export let choices = [];
  export let step = 1 || null;
  export let css = "";
  export let style="";
  export let size= "" || null;
  const inputProperties = { type };
  let requiredClass = required ? "required" : ""; 

  $: hasErrors = errors && errors[name];
  $: errorClass = hasErrors ? "variant-ringed-error" : "";

  const handleInput = e => {
      value = e.target.value;
  };

  export let baseClass : string = undefined;
  let baseClassLookup = {
      textarea: "textarea",
      file: "",
      select: "select",
      input: "input"
  }

  if (baseClass === undefined){
      baseClass = baseClassLookup[type] || "input"; 
  }

</script>
{#if type === "textarea"}
  <!-- <textarea
  {...inputProperties}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  {name}
  style="{style}"
  class="{baseClass} {errorClass} {css}"
  bind:value
  on:input={handleInput} /></textarea> -->
{:else if type === "duration"}
<DurationField bind:value name={name}></DurationField>
{:else if type === "file"}
  <input
  {...inputProperties}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  {name}
  style="{style}"
  class="{baseClass} {errorClass} {css}"
  bind:value
  on:input={handleInput} />
{:else if type === "select"}
  <select
  {...inputProperties}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  {name}
  style="{style}"
  class="{baseClass} {errorClass} {css}"
  bind:value
  on:input={handleInput}>
      {#each choices as choice}
      <option value="{choice}">{choice}</option>
      {/each}
  </select>
{:else}
  <input
  {...inputProperties}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  step={step}
  {name}
  size={size}
  style="{style}"
  class="{baseClass} {errorClass} {css}"
  bind:value
  on:input={handleInput} />
{/if}
<slot name="after">

</slot>