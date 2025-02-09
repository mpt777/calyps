<script lang="ts">
  import { Tooltip } from '@skeletonlabs/skeleton-svelte';
  let openState = $state(false);
  let {_trigger, _content} = $props();
</script>

<Tooltip
  bind:open={openState}
  positioning={{ placement: 'top' }}
  triggerBase=""
  contentBase="card preset-filled p-4"
  openDelay={50}
  closeDelay={50}
>
  {#snippet trigger()}{@render _trigger({type:"button"})}{/snippet}
  {#snippet content()}{@render _content()}{/snippet}
</Tooltip>