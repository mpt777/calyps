<script>
    import { fly, slide } from "svelte/transition";

  let { message, level } = $props();
</script>

{#if message}
<div class="p-4 rounded preset-filled-{level}-500" in:fly={{y:-10, duration:100,opacity:100}}>
  {message}
</div>
{/if }