<script lang="ts">
  import { Portal, Tooltip } from '@skeletonlabs/skeleton-svelte';
  let { _trigger, _content } = $props();
</script>

<Tooltip positioning={{ placement: 'top' }} openDelay={50} closeDelay={50}>
  <Tooltip.Trigger>
    {#snippet element({ type, ...attributes }: Record<string, any>)}
      <span {...attributes} class="inline-flex">{@render _trigger()}</span>
    {/snippet}
  </Tooltip.Trigger>
  <Portal>
    <Tooltip.Positioner class="z-50!">
      <Tooltip.Content class="card preset-filled p-4">{@render _content()}</Tooltip.Content>
    </Tooltip.Positioner>
  </Portal>
</Tooltip>
