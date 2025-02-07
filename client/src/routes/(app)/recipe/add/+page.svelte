<script lang="ts">
  let { data, form } = $props();

  import { enhance } from '$app/forms';
  import Field from '$components/form/Field.svelte';
  import Message from '$components/message/Message.svelte';
    import Recipe from '$components/recipe/Recipe.svelte';
    import RecipeEdit from '$components/recipe/RecipeEdit.svelte';
  import { url } from '$utils/url.js';

</script>

<form method="POST" use:enhance>

	<RecipeEdit form={form} data={data}/>
</form>