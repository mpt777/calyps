<script>
	import { url } from '$utils/url.js';
	import { fly, fade } from 'svelte/transition';

	let { data } = $props();

	let inputedName = $state("");
	let giftee = $state("");
	let toggle = $state(false);

	console.log(data)
	const lookup = Object.fromEntries(
		Object.entries(data.pairs_str).map(([k, v]) => [k.toLowerCase(), v])
	);

	$effect(() => {
		if (!lookup[inputedName.trim().toLowerCase()]) {
			giftee = "";
		}
	});

	function findGiftee() {
		let name = inputedName.trim().toLowerCase();
		toggle = !toggle;
		giftee = lookup[name] ?? "Not Found";
	}
</script>
<div class="flex justify-center">
	<div class="calyps--card">
		<header class="card-header p-4 bg-surface-200-700-token ">
			<h2 class="h2">
				Secret Santa
			</h2>
		</header>
		<hr>
		
		<section class="p-4">Welcome to Secret Santa: {data.name}</section>
		<section class="p-4">Please enter your name (case insesitive) to reveal who will be your giftee!</section>
		<section class="p-4 space-y-4">

			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<div class="input-group-cell preset-tonal-surface">Your Name</div>
				<input type="text" class="input--min-w-4" bind:value={inputedName}/>
				<a class="btn h-full preset-filled-primary-500 rounded-none cursor-pointer" onclick="{() => findGiftee()}">Find!</a>
			</div>

			<div class="flex justify-center">
				<div class="text-center">
					<div>Your Giftee</div>
					<div class="text-5xl h-[4rem]">
						{#key toggle}
						<div in:fade={{ duration: 200 }}>
							<div in:fly={{ y: -10, duration: 200 }}>{giftee}</div>
						</div>
						{/key}
					</div>
					<div></div>
				</div>
			</div>


		</section>
		<hr>
		<footer class="card-footer p-4 flex justify-between">
			<div>
			</div>
				<a href="{url("projects")}" class="btn variant-ghost float-right"><i class="ri-arrow-left-line"></i> Return</a>
		</footer>
	</div>
</div>