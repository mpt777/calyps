<script>
    import { page } from "$app/state";
    import RecipeCardList from "$components/recipe/RecipeCardList.svelte";
    import { Tabs } from "@skeletonlabs/skeleton-svelte";

    let {data} = $props();

    let group = $state("recipe")
</script>


<svelte:head>
  <title>My Profile</title>
</svelte:head>



<div class="grid grid-cols-12 gap-4">
  <div class="col-span-12 md:col-span-8">

    <Tabs value={group} onValueChange={(e) => (group = e.value)}>
      <Tabs.List>
        <Tabs.Trigger value="recipe">Recipe</Tabs.Trigger>
        <Tabs.Trigger value="saved">Saved</Tabs.Trigger>
        <Tabs.Trigger value="collection">Collections</Tabs.Trigger>
        <Tabs.Indicator />
      </Tabs.List>
      <Tabs.Content value="recipe">
        <RecipeCardList recipes={data.paginator.results}></RecipeCardList>
      </Tabs.Content>
      <Tabs.Content value="saved">
        Todo
      </Tabs.Content>
      <Tabs.Content value="collection">
        Todo
      </Tabs.Content>
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
            <dd class="text-muted">{data.profile.username}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Name</dt>
            <dd class="text-muted">{data.profile.first_name} {data.profile.last_name}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Email</dt>
            <dd class="text-muted">{data.profile.email}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Since</dt>
            <dd class="text-muted">{new Date(data.profile.date_joined).toLocaleDateString()}</dd>
          </div>
          <div class="dl-horizontal">
            <dt class="">Last Login</dt>
            <dd class="text-muted">{new Date(data.profile.last_login).toLocaleString()}</dd>
          </div>
        </dl>

      </section>
    </div>

  </div>

</div>
