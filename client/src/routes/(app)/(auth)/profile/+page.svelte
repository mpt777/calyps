<script>
    import { page } from "$app/state";
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";
    import { Tabs } from "@skeletonlabs/skeleton-svelte";

    let {data} = $props();

    let group = $state("recipe")
</script>

<style>
  .dl-horizontal {
    @apply px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0;
  }
  .dl-horizontal>dt {
    @apply text-sm font-medium text-gray-900;
  }
  .dl-horizontal>dd  {
    @apply mt-1 text-sm text-gray-700 sm:col-span-2 sm:mt-0;
  }
</style>



<div class="grid grid-cols-12 gap-4">
  <div class="col-span-12 md:col-span-8">

    <Tabs bind:value={group}>
      {#snippet list()}
        <Tabs.Control value="recipe">Recipe</Tabs.Control>
        <Tabs.Control value="saved">Saved</Tabs.Control>
        <Tabs.Control value="collection">Collections</Tabs.Control>
      {/snippet}
      {#snippet content()}
        <Tabs.Panel value="recipe">
          <RecipeCardList recipes={data.paginator.results}></RecipeCardList>
        </Tabs.Panel>
        <Tabs.Panel value="saved">
          Todo
        </Tabs.Panel>
        <Tabs.Panel value="collection">
          Todo
        </Tabs.Panel>
      {/snippet}
    </Tabs>
    
    
  </div>
  <div class="col-span-12 md:col-span-4">

    <div class="calyps--card">
      <section class="p-4">
        <h3 class="h3">Profile</h3>
      </section>
      <hr>
      <section class="p-4">
        <dl class="divide-y divide-gray-100">
          <div class="dl-horizontal">
            <dt class="">Username</dt>
            <dd class="">{data.profile.username}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Name</dt>
            <dd class="">{data.profile.first_name} {data.profile.last_name}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Email</dt>
            <dd class="">{data.profile.email}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Since</dt>
            <dd class="">{new Date(data.profile.date_joined).toLocaleDateString()}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Last Login</dt>
            <dd class="">{new Date(data.profile.last_login).toLocaleString()}</dd>
          </div>
        </dl>

      </section>
    </div>

  </div>

</div>
