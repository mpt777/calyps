<script>
  // @ts-nocheck
    let {input, error, errors, value=$bindable(), placeholder="", label="", name, forName="", autocomplete="", required=false, choices=[], constraints=[], type="text", css="", baseClass=undefined, form=undefined} = $props();
      import Input from "./Input.svelte";
      import Errors from "./Errors.svelte";
  
    // let errors = $derived(form?.errors);

    let requiredClass = required ? "required" : ""; 
    let hasErrors = errors && errors[name];
    let classes = hasErrors ? "with-error" : "";

  </script>
  
  
  <label class="label" for="{name || forName}">
    {value}
      {#if label}
          <span class="label-text {requiredClass}">{label}</span>
      {/if}

      {#if input}
        {@render input()}
      {:else}
        {#if name}<Input bind:value={value} placeholder={placeholder} name={name} autocomplete={autocomplete} type={type} classes={classes} required={required} baseClass={baseClass} {...constraints} choices={choices} css={css}/>{/if}
      {/if}

      {#if error}
        {@render error()}
      {:else}
        {#if errors?.[name]}<Errors error="{errors?.[name]}" />{/if}
      {/if}
      
  </label>