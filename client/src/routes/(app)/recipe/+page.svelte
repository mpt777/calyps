<script>
    import { page } from "$app/state";
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";
    import { url } from "$utils/url.js";
    import path from "path";

  let {data} = $props();

</script>

<svelte:head>
  <title>Recipe List</title> 
</svelte:head>

<div class="flex items-center gap-4 justify-center">
  <div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x items-center">
    <button type="button">
      <i class="ri-search-line p-4"></i>
    </button>

    <input type="text" name="search" placeholder="Search">

  </div>
  {#if page.data.user}
  <div class="text-center">
    <a class="preset-filled-tertiary-500 btn btn--scale" href="{url('recipe_add')}">Add Recipe <i class="ri-sticky-note-add-fill"></i></a>
  </div>
  {:else}
  <div class="text-center">
    <a class="preset-filled-tertiary-500 btn btn--scale " href="/login?redirectTo={page.url.pathname}">Please Login to Add Recipe</a>
  </div>
  {/if}
</div>
<RecipeCardList recipes={data.recipes}></RecipeCardList>