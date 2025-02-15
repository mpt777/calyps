<script>
    import RecipeEdit from "$components/recipe/RecipeEdit.svelte";

  let {data, form} = $props();
  console.log(data)
</script>
<div>
  <RecipeEdit data={data} form={form}/>
</div>