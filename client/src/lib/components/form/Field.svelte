<script>
  // @ts-nocheck
  import Input from "./Input.svelte";
  import Errors from "./Errors.svelte";

    let {
      value=$bindable(), 
      name, 
      label="", 
      forName="", 
      input=null, 
      error=null, 
      errors, 
      placeholder="", 
      autocomplete="", 
      required=false, 
      choices=[], 
      constraints=[], 
      type="text", 
      css="",
      form=undefined
    } = $props();

  
    // let errors = $derived(form?.errors);

    let requiredClass = required ? "required" : ""; 
    let hasErrors = errors && errors[name];
    let classes = hasErrors ? "with-error" : "";

  </script>
  <label class="label" for="{name || forName}">
      {#if label}
          <span class="label-text {requiredClass}">{label}</span>
      {/if}

      {#if input}
        {@render input()}
      {:else}
        {#if name}<Input bind:value={value} placeholder={placeholder} name={name} autocomplete={autocomplete} type={type} classes={classes} required={required} {...constraints} choices={choices} css={css}/>{/if}
      {/if}

      {#if error}
        {@render error()}
      {:else}
        {#if errors?.[name]}<Errors error={errors?.[name]}/>{/if}
      {/if}
      
  </label>