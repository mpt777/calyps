<script>
    import DurationField from "./DurationField.svelte";

  let {errors={}, value=$bindable(), placeholder="", label="", name="", forName="", autocomplete="", required=false, choices=[], _choices="", constraints=[], type="text", css="", form=undefined, step=1, multiple=false, accept=""} = $props();
  const inputProperties = $derived({ type });

  let requiredClass = required ? "required" : ""; 
  let hasErrors = errors && errors[name];
  let classes = hasErrors ? "with-error" : "";
  let errorClass = hasErrors ? "variant-ringed-error" : "";

  // const handleInput = e => {
  //     value = e.target.value;
  // };

  let baseClassLookup = {
      textarea: "textarea",
      file: "",
      select: "select",
      input: "input"
  }

  let baseClass = baseClassLookup[type] || "input";

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
{:else if type === "checkbox"}
  <input
  {name}
  style="{css}"
  class="{baseClass} {errorClass}"
  type="checkbox"
  bind:checked={value}/>
{:else if type === "file"}
  <input
  {...inputProperties}
  multiple={multiple}
  accept={accept}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  {name}
  style="{css}"
  class="{baseClass} {errorClass} {css}"
  bind:value={value}/>
{:else if type === "select"}
  <select
  {...inputProperties}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  {name}
  style="{css}"
  class="{baseClass} {errorClass} {css}"
  bind:value>
  {#if _choices}
    {@render _choices()}
  {:else}
      {#if !required}<option value="">---</option>{/if}
      {#each choices as choice}
      <option value="{choice.value}">{choice.name}</option>
      {/each}
  {/if}
  </select>
{:else}
  <input
  {...inputProperties}
  placeholder={placeholder}
  autocomplete={autocomplete}
  required={required}
  step={step}
  {name}
  style="{css}"
  class="{baseClass} {errorClass} {css}"
  aria-invalid={hasErrors ? 'true' : undefined}
  bind:value />
{/if}