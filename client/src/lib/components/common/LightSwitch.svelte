<script lang="ts">
    import { localStore } from "$scripts/localStorage.svelte";
    import { onMount } from "svelte";

	let darkMode = localStore('count', false);
	// let darkMode = $state(false);

	onMount(() => {
			if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
				darkMode.value = true;
			}
			update();
	})


	function toggleDarkMode() {
		darkMode.value = !darkMode.value;
		update();
	}

	function update() {
		darkMode.value ? document.documentElement.classList.add('dark') : document.documentElement.classList.remove('dark');
		darkMode.value ? document.documentElement.setAttribute('data-mode', "dark") : document.documentElement.removeAttribute('data-mode');
	}

  
</script>

<button class="btn btn-icon preset-outlined-surface-200-800 hover:preset-tonal" onclick={toggleDarkMode}>
	{#if darkMode.value}
	<i class="ri-sun-line"></i>
	
	{:else }
	<i class="ri-moon-line"></i>
	{/if }
</button>