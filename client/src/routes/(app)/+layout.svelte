<script>
	// import { AppShell, AppBar, Drawer, Toast, Avatar} from '@skeletonlabs/skeleton';
	import { page } from '$app/state';
	import Navigation from '$components/nav/Navigation.svelte';
	import ToastMessage from '$components/message/MessageToast.svelte';


	import { browser } from '$app/environment';
	// import { LightSwitch } from '@skeletonlabs/skeleton';
	import { onMount, setContext } from 'svelte';
    import LightSwitch from '$components/common/LightSwitch.svelte';
    import Drawer from '$components/common/Drawer.svelte';
    import Tooltip from '$components/common/Tooltip.svelte';
    import { Avatar } from '@skeletonlabs/skeleton-svelte';
    import { url } from '$utils/url';
	// import Input from '$components/form/Input.svelte';

	// import { getDrawerStore } from "@skeletonlabs/skeleton";
	// import { popup } from '@skeletonlabs/skeleton';
	
	// import type { PopupSettings } from '@skeletonlabs/skeleton';
	// import Breadcrumb from '$components/utils/Breadcrumb.svelte';

	let { children } = $props();

	let breadcrumbs = $derived(page.data.breadcrumbs || []);

	let drawerState = $state(false);
	setContext('drawerState', drawerState);
</script>

<svelte:head>
	<title>Calyps.io</title>
</svelte:head>

<!-- <Toast position="tr" /> -->
<!-- <Modal /> -->

{#if browser}
<ToastMessage />
{/if }

<div class="flex flex-col h-screen overflow-hidden">
	<!-- Header -->
	<header class="bg-surface-50-900-token p-4 shadow-md z-10">
		<div class="flex justify-between">
		  <div class="h4"><a href="/">Calyps.io</a></div>
		  <div class="flex gap-4 items-center">

				{#if page.data.user}
				<a href="{url('profile')}" class="cursor-pointer">
					<Avatar
						name={page.data.user.username?.charAt(0)}
						border="border-4 border-surface-300-600-token hover:!border-primary-500"
						size="size-10"
					/>
				</a>
				{/if}

				<LightSwitch/>

				<Drawer >
					{#snippet _trigger()}
					<i class="ri-menu-line"></i>
					{/snippet}
					{#snippet _content()}
					<div class="p-0 pb-4 pt-8 h-full"><Navigation/></div>
					{/snippet}
				</Drawer>


				
			</div>
		</div>
	</header>
	<!-- Grid Columns -->
	<div class="flex h-full overflow-hidden">
	  <!-- Left Sidebar. -->
	  <aside class="p-4 bg-surface-50-900-token hidden md:block border-r border-surface-500/30 ">
      <Navigation/>
    </aside>
	  <!-- Main Content -->
    <div class="flex justify-between flex-col overflow-y-auto w-full">
      <main class="space-y-4 p-4">
        {@render children()}
      </main>
      <footer class="p-4 bg-surface-500/20">
        <div class="flex justify-between">
          <div></div>
          <div class="text-xl">

							<Tooltip>
								{#snippet _content()}
								<div class="text-sm">
									<div><p>View the Legacy <br>Emptytxt.com</p></div>
									<div class="arrow bg-surface-100-800-token"></div>
								</div>
								{/snippet}
								{#snippet _trigger()}
								<a href="https://emptytxt.com" aria-label="Legacy Site">
									<img src="/favicon.ico" class="inline w-4 pb-1" alt="emptytx logo">
								</a>
								{/snippet}
							</Tooltip>

						<a href="https://www.youtube.com/@mpt777" aria-label="Youtube">
              <i class="ri-youtube-fill"></i>
            </a>

            <a href="https://github.com/mpt777" aria-label="GitHub">
              <i class="ri-github-fill"></i>
            </a>
          </div>
        </div>
	    </footer>
    </div>

	</div>
	
</div>
