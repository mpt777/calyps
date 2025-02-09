<script>
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";

  let {data} = $props();

</script>


<RecipeCardList recipes={data.recipes}></RecipeCardList>