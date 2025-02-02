<script>
  import { page } from '$app/state';
  import { drawerState } from '$scripts/globalState.svelte';
  import { getContext, setContext } from 'svelte';
  
  let {title="", href, children=null} = $props();

  let url = $state(page);

  let classes = $derived.by(() => url.url.pathname == href ? "rounded preset-tonal" : "")

  function click() {
    drawerState.open = false;
  }
  
  
</script>

<a href="{href}"  class="anchor w-full px-2 py-1 rounded {classes} inline-block" onclick={click}>
  {title}
  {#if children }
  {@render children()}
  {/if}
</a>