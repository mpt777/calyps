<script lang="ts">
	import { setContext } from 'svelte';

	
	import { Modal } from '@skeletonlabs/skeleton-svelte';
	import { drawerState } from '$scripts/globalState.svelte';


  let {_trigger, _content} = $props();
</script>

<!--
Tips for Drawer modals:
- Use `contentBase` to set styles, including height/width
- Set justify-start to align to the left
- Clear the align and padding styles
- Use `positionerClasses` to set the
- Set transition.x values that matches content width in pixels
-->

<Modal
	bind:open={drawerState.open}
	triggerBase="btn preset-tonal"
	contentBase="bg-surface-100-900 p-4 shadow-xl w-[200px] h-100"
	positionerJustify="justify-start"
	positionerAlign=""
	positionerPadding=""
	transitionsPositionerIn={{ x: -200, duration: 200 }}
	transitionsPositionerOut={{ x: -200, duration: 200 }}
>
	{#snippet trigger()}{@render _trigger()}{/snippet}
	{#snippet content()}
	<div class="relative h-full">
		<button class="btn preset-tonal absolute top-0 right-0" onclick={() => drawerState.open = false} aria-label="Toggle Drawer">
				<i class="ri-close-large-line"></i>
		</button>


		{@render _content()}
	</div>
	{/snippet}
</Modal>