<script lang="ts">
  let { data } = $props();

	let recipe = data.recipe;

    import Recipe from '$components/recipe/Recipe.svelte';

</script>

<svelte:head>
	<title>{recipe.name}</title>
</svelte:head>

<Recipe recipe={recipe}/>