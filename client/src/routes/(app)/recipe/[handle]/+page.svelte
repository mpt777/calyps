<script lang="ts">
  let { data, form } = $props();

	let recipe = data.recipe;

  import { enhance } from '$app/forms';
  import Field from '$components/form/Field.svelte';
  import Message from '$components/message/Message.svelte';
    import Recipe from '$components/recipe/Recipe.svelte';
  import { url } from '$utils/url.js';

</script>

<svelte:head>
	<title>{recipe.name}</title>
</svelte:head>

<Recipe recipe={recipe}/>