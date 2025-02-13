<script>
    import RecipeEdit from "$components/recipe/RecipeEdit.svelte";

  let {data, form } = $props();

</script>

<svelte:head>
  <title>Add Recipe</title> 
</svelte:head>
<div>
  <RecipeEdit data={data} form={form} />
</div>