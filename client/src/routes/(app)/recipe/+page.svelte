<script>
    import { goto, replaceState } from "$app/navigation";
    import { page } from "$app/state";
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";
    import { iapi, papi } from "$utils/api";
    import { debounce } from "$utils/form";
    import { url } from "$utils/url.js";
    import path from "path";
    import { onMount } from "svelte";

    let {data} = $props();

    let search = $state("");
    let paginator = $state(data.paginator)

    $effect(() =>{
      paginator = data.paginator
    })

    async function getData() {
      page.url.searchParams.set('search', search);
      page.url.searchParams.set('page', "1"); 
      history.replaceState(page.state, "", page.url.toString());

      let response = await iapi(
        `recipe/search/recipe/?${page.url.searchParams.toString()}`,
        { method: "GET" }
      );
      paginator = await response.json();
      console.log(paginator);
    }

</script>

<svelte:head>
  <title>Recipe List</title> 
</svelte:head>

<div class="flex items-center gap-4 justify-center">
  {#if paginator.previous}
  <a href="{page.url.pathname}?{(data.paginator.previous || "").split("?")[1]}" class="anchor">
    Previous
  </a>
  {:else}
    <span class="text-gray-400 cursor-not-allowed">Previous</span>
  {/if}

  <form method="GET">
    <div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x items-center">
      <button type="submit" aria-label="Search">
        <i class="ri-search-line p-4"></i>
      </button>

      <input type="text" name="search" placeholder="Search" oninput={debounce(getData, 300)} bind:value={search}>
    </div>
  </form>
  {#if page.data.user}
  <div class="text-center">
    <a class="preset-filled-tertiary-500 btn btn--scale" href="{url('recipe_add')}">Add Recipe <i class="ri-sticky-note-add-fill"></i></a>
  </div>
  {:else}
  <div class="text-center">
    <a class="preset-filled-tertiary-500 btn btn--scale " href="/login?redirectTo={page.url.pathname}">Please Login to Add Recipe</a>
  </div>
  {/if}

  {#if paginator.next}
  <a href="{page.url.pathname}?{(paginator.next|| "").split("?")[1]}" class="anchor">
    Next
  </a>
  {:else}
    <span class="text-gray-400 cursor-not-allowed">Next</span>
  {/if}

</div>
<RecipeCardList recipes={paginator.results}></RecipeCardList>