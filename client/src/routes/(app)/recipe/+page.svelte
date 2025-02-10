<script>
    import { page } from "$app/state";
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";

  let {data} = $props();

</script>

<svelte:head>
  <title>Recipe List</title> 
</svelte:head>

{#if page.data.user}
<div class="text-center">
  <a class="preset-filled-tertiary-500 btn" href="/recipe/add">Add Recipe <i class="ri-sticky-note-add-fill"></i></a>
</div>
{:else}
<div class="text-center">
  <a class="preset-filled-tertiary-500 btn" href="/login">Please Login to Add Recipe</a>
</div>
{/if}
<RecipeCardList recipes={data.recipes}></RecipeCardList>