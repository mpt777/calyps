<script>
	import { Dialog, Portal } from "@skeletonlabs/skeleton-svelte";
	import Navigation from '$components/nav/Navigation.svelte';
	import { drawerState } from '$scripts/globalState.svelte';

	let {} = $props();

	const animBackdrop = 'transition transition-discrete opacity-0 starting:data-[state=open]:opacity-0 data-[state=open]:opacity-100';
	const animModal =
		'transition transition-discrete opacity-0 -translate-x-full starting:data-[state=open]:opacity-0 starting:data-[state=open]:-translate-x-full data-[state=open]:opacity-100 data-[state=open]:translate-x-0';

</script>
<Dialog open={drawerState.open}>
	<Dialog.Trigger class="btn btn-icon preset-outlined-surface-200-800 hover:preset-tonal md:hidden" onclick={() => drawerState.open = !drawerState.open}>
		<i class="ri-menu-line"></i>
	</Dialog.Trigger>
	<Portal>
		<Dialog.Backdrop class="fixed inset-0 z-50 bg-surface-50-950/50 transition transition-discrete {animBackdrop}" />
		<Dialog.Positioner class="fixed inset-0 z-50 flex justify-start">
			<Dialog.Content class="h-screen card bg-surface-100-900 w-sm p-4 space-y-4 shadow-xl {animModal}">
					<Dialog.CloseTrigger class="btn-icon preset-tonal float-right" onclick={() => drawerState.open = false}>
						<i class="ri-close-large-fill"></i>
					</Dialog.CloseTrigger>
				<div class="p-0 pb-4 pt-8 h-full"><Navigation/></div>
			</Dialog.Content>
		</Dialog.Positioner>
	</Portal>
</Dialog>
