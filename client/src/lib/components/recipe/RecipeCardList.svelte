<script>
  import RecipeCard from "./RecipeCard.svelte";
  let {recipes} = $props();
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
{#each recipes as recipe}
  <RecipeCard recipe={recipe}></RecipeCard>
{/each}
</div>