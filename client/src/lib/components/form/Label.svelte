<script>
  let {name="", label, required=false} = $props();
  let requiredClass = required ? "required" : ""; 
</script>

<label class="label" for="{name}">
  {#if label}
      <span class="label-text {requiredClass}">{label}</span>
  {/if}
</label>