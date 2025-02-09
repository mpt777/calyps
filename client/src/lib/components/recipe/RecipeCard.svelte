<script>
    import { page } from "$app/state";
    import Tooltip from "$components/common/Tooltip.svelte";
    import QuillDisplay from "$components/form/QuillDisplay.svelte";
    import { formatTimeString } from "$scripts/humanize";
    import { url } from "$utils/url";

  let {recipe} = $props();

</script>
		
<div class="calyps--card max-w-sm w-full mx-auto" >
  <header class="card-header p-4 bg-surface-200-700-token ">
    <div class="flex justify-between items-center">
      <h3 class="h3">
        {recipe.name}
      </h3>
      <div>
        {recipe.created_by}
      </div>
    </div>

  </header>
  <hr>

  <section class="p-2 space-y-4 text-sm">
    <QuillDisplay content={recipe.description}></QuillDisplay>
  </section>

  <hr>

  <section class="p-2">
    <div class="flex justify-around text-xs">
      <div class="text-center">
          <div class="font-bold">Cook Time:</div>
          <div>{formatTimeString(recipe.cook_time)}</div>
      </div>
      <div class="text-center">
          <div class="font-bold">Prep Time:</div>
          <div>{formatTimeString(recipe.prep_time)}</div>
      </div>
      <div class="text-center">
          <div class="font-bold">Servings:</div>
          <div>{recipe.servings}</div>
      </div>
    </div>
  </section>

  <hr>

  <footer class="card-footer p-4 space-y-4">
    <div class=" flex justify-center gap-1 align-center">
      <a href="{url('recipe', {handle:recipe.handle})}" class="btn preset-filled-secondary-500 w-full" type="submit">View</a>
      {#if page.data.user?.username === recipe.created_by}
      <div>
          <Tooltip>
              {#snippet _content()}
              <div class="text-sm">
                  Edit Recipe
              </div>
              {/snippet}
              {#snippet _trigger()}
              <!-- <a href="{url("recipe_edit", {handle:recipe.handle})}" class="btn btn-sm variant-filled-tertiary"> -->
              <a href="/recipe/edit/{recipe.handle}" class="btn btn-sm variant-filled-tertiary" aria-label="Edit Recipe">
                  <i class="ri-pencil-line text-lg"></i>
              </a>
              {/snippet}
          </Tooltip>
      </div>
      {/if}
    </div>

  </footer>
</div>