<script>
  import RecipeEdit from "$components/recipe/RecipeEdit.svelte";
  import ScanRecipe from "$components/recipe/ScanRecipe.svelte";
  import { draftToForm } from "$components/recipe/scanDraft";

  let { data, form } = $props();

  // A scanned draft replaces the starting values (data.form is only the
  // starting point, so capturing it once is intended); bumping `version` remounts
  // the form so every field (editors, durations, tags) picks them up.
  // svelte-ignore state_referenced_locally
  let initial = $state(data.form);
  let version = $state(0);

  /** @param {import("$components/recipe/scanDraft").RecipeDraft} draft */
  function applyDraft(draft) {
    initial = draftToForm(draft, data.form, data.units);
    version += 1;
  }
</script>

<svelte:head>
  <title>Add Recipe</title>
</svelte:head>
<div>
  <ScanRecipe onDraft={applyDraft} />
  {#key version}
    <RecipeEdit data={{ ...data, form: initial }} {form} />
  {/key}
</div>
