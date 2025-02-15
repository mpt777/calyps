<script>
    import { goto, replaceState } from "$app/navigation";
    import { page } from "$app/state";
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";
    import { iapi, papi } from "$utils/api";
    import { debounce } from "$utils/form";
    import { url } from "$utils/url.js";
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

<div class="flex items-center justify-center">
  <div class="grid grid-cols-1 md:grid-cols-3 items-center gap-4 justify-center">

    <span class="hidden md:block justify-self-end">
      {#if paginator.previous}
      <a href="{page.url.pathname}?{(data.paginator.previous || "").split("?")[1]}" class="anchor">
        Previous
      </a>
      {:else}
        <span class="text-gray-400 cursor-not-allowed">Previous</span>
      {/if}
    </span>

    <form method="GET">
      <div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x items-center">
        <button type="submit" aria-label="Search">
          <i class="ri-search-line p-4"></i>
        </button>

        <input type="text" name="search" placeholder="Search" oninput={debounce(getData, 300)} bind:value={search}>

        <div class="text-center h-full">
        {#if page.data.user}
          <a class="preset-filled-tertiary-500 btn btn--scale h-full" href="{url('recipe_add')}">Add Recipe <i class="ri-sticky-note-add-fill"></i></a>
        {:else}
          <a class="preset-filled-tertiary-500 btn btn--scale h-full" href="/login?redirectTo={page.url.pathname}">Login</a>
        {/if}
      </div>
      </div>

    </form>


    <div class="flex gap-2 md:justify-self-start justify-around">
      <span class="md:hidden">
        {#if paginator.previous}
        <a href="{page.url.pathname}?{(data.paginator.previous || "").split("?")[1]}" class="anchor">
          Previous
        </a>
        {:else}
          <span class="text-gray-400 cursor-not-allowed">Previous</span>
        {/if}
      </span>
      {#if paginator.next}
      <a href="{page.url.pathname}?{(paginator.next|| "").split("?")[1]}" class="anchor">
        Next
      </a>
      {:else}
        <span class="text-gray-400 cursor-not-allowed">Next</span>
      {/if}
    </div>

  </div>
</div>
<RecipeCardList recipes={paginator.results}></RecipeCardList>