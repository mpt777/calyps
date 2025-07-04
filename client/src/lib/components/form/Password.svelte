<script>
    import Input from "./Input.svelte";
    import Label from "./Label.svelte";
  
    let shown = $state(false);
    let inputType = $derived.by(() => {
      console.log(shown)
      return shown ? "text" : "password"
    })

</script>
<div>
  <Label label="Password" required={true}></Label>
  <div class="input-group divide-surface-200-800 flex divide-x">
    <Input name="password" placeholder="Password" label="Password" autocomplete="new-password" required={true} type={inputType} css="w-full!"/>
    <button type="button" class="w-fit! px-4" onclick={() => shown = !shown}>
      {#if shown}
      <i class="ri-eye-off-line"></i>
      
      {:else}
      <i class="ri-eye-line"></i>
      {/if}
    </button>
  </div>
</div>