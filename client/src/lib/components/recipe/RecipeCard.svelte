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

  {#if recipe.tag_types}
  <section class="p-2 pt-0">
    <div class="flex gap-1">
      {#each recipe.tag_types as tag_type}
      <div class="chip preset-filled ">{tag_type}</div>
      {/each}
    </div>
  </section>
  {/if}

  <hr>

  <section class="p-2">
    <div class="flex justify-around text-xs">
      <div class="text-center">
          <div>
            <i class="ri-time-line"></i>
            {formatTimeString(recipe.cook_time + recipe.prep_time)}
          </div>
      </div>
      <div class="text-center">
          <i class="ri-group-line"></i>
          <span>Servings:</span> {recipe.servings}
      </div>
    </div>
  </section>

  <section class="p-2 space-y-4 text-sm">
    <QuillDisplay content={recipe.description}></QuillDisplay>
  </section>

  <hr>

  <footer class="card-footer p-4 space-y-4">
    <div class=" flex justify-center gap-1 align-center">
      <a href="{url('recipe', {handle:recipe.handle})}" class="btn preset-filled-primary-500 w-full" type="submit">View</a>
      {#if page.data.user?.username === recipe.created_by}
      <div>
          <Tooltip>
              {#snippet _content()}
              <div class="text-sm">
                  Edit Recipe
              </div>
              {/snippet}
              {#snippet _trigger()}
              <div class="flex align-center h-full">
                <a href="{url("recipe_edit", {handle:recipe.handle})}" class="btn btn-sm variant-filled-primary">
                <!-- <a href="/recipe/{recipe.handle}/edit" class="btn btn-sm variant-filled-tertiary" aria-label="Edit Recipe"> -->
                    <i class="ri-pencil-line text-lg"></i>
                </a>
              </div>
              {/snippet}
          </Tooltip>
      </div>
      {/if}
    </div>

  </footer>

</div>