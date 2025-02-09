<script>
  import Tooltip from "$components/common/Tooltip.svelte";
  import Field from "$components/form/Field.svelte";
  import Quill from "$components/form/Quill.svelte";
  import Message from "$components/message/Message.svelte";
    
  import { url } from "$utils/url";

  import SuperDebug from 'sveltekit-superforms';
  import { superForm } from 'sveltekit-superforms/client'

  function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  import { reorder, useSortable } from "$scripts/useSortable.svelte";
  import { enhance } from "$app/forms";
    import { generateHandle } from "$scripts/humanize";
    import Input from "$components/form/Input.svelte";

  let {data, form} = $props();

  // const { form: formData, errors, constraints, message, enhance } = superForm(formData, {
  //   customValidity: true,
  //   dataType: 'json'
  // });


  let visibilityChoices = data.visbilities.map(e => {
    return {"value": e.id, "name": e.name}
  })

  let unitChoices = data.units.map(e => {
    return {"value": e.id, "name": e.name}
  })

  let formData = $state(data.form)


  $effect(() => {
    setHandle()
  })

  function setHandle() {
    if (!formData.id) {
      formData.handle = generateHandle(formData.name)
    }
    formData.handle = generateHandle(formData.handle)
  }

  //-------------------------------------------

  formData.ingredients = formData.ingredients || []

  formData.ingredients.forEach(e=>{
    e.u=generateUUID();
  })

  let sortable = $state(null);

  useSortable(() => sortable, {
    animation: 200,
    handle: '.my-handle',
    ghostClass: 'opacity-0',
    onEnd(evt) {
      formData.ingredients = reorder(formData.ingredients, evt);
      sortIngredients()
    }
  });

  function sortIngredients() {
    let counter = 1
    formData.ingredients.forEach((_, i) => {
      let value = 0
      if (!formData.ingredients[i].DELETE) {
        value = counter
        counter++
      }
      formData.ingredients[i].sequence = value
    })
    formData.ingredients = [...formData.ingredients]
  }

  function addIngredient() {
    console.log("here")
    formData.ingredients.push({
      name: "",
      amount: 0,
      unit: data.units[0].id,
      sequence: 0,
      u: generateUUID(),
      DELETE:false
    })
    sortIngredients()
    formData.ingredients = formData.ingredients
  }

  async function removeIngredient(item, i) {
    formData.ingredients[i].DELETE=true;
    formData.ingredients[i].amount=1;
    formData.ingredients[i].name="DELETE";
    sortIngredients()
  }
</script>
<!-- <pre class="mt-5 w-fit border p-5">{JSON.stringify(formData, null, 2)}</pre>
<pre class="mt-5 w-fit border p-5">{JSON.stringify(form, null, 2)}</pre> -->


<form method="POST" use:enhance class="space-y-4">

  <input name="hack" value={JSON.stringify(formData)} class="hidden">
  <Message message={ form?.message } level={form?.level}/>

<div class="flex gap-8 max-w-screen-lg mx-auto flex-wrap md:flex-nowrap ">
  <div class="w-full">
    <div class="calyps--card w-full bg-surface-50-950">
      <header class="card-header p-4 bg-surface-200-700-token ">
        <div class="flex justify-between items-center">
          <h2 class="h2">Recipe</h2>
          <div>
            <Tooltip>
              {#snippet _content()}
              <div class="text-sm">
                  View Recipe
              </div>
              {/snippet}
              {#snippet _trigger()}
              <a href={url("recipe", {handle: data.form.handle})} class="anchor">
                <i class="ri-eye-line"></i>
              </a>
              {/snippet}
            </Tooltip>
          </div>
        </div>
        
      </header>
      <hr>
      <section class="p-4 space-y-4">
        <div class="grid grid-cols-12 md:gap-8">
          <div class="col-span-12 md:col-span-8">
            <Field name="name" placeholder="Name" label="Name" required={true} bind:value={formData.name} errors={form?.errors}/>
          </div>
          <div class="col-span-12 md:col-span-4">
            <Field name="servings" placeholder="Servings" label="Servings" required={true} bind:value={formData.servings} errors={form?.errors} type="number"/>
          </div>
        </div>

        <div class="grid grid-cols-12 md:gap-8">
          <div class="col-span-12 lg:col-span-6">
            <Field name="prep_time"  label="Prep Time" required={true} type="duration" bind:value={formData.prep_time} errors={form?.errors}/>

          </div>
          <div class="col-span-12 lg:col-span-6">
            <Field name="cook_time" label="Cook Time" required={true} type="duration" bind:value={formData.cook_time} errors={form?.errors}/>
          </div>
        </div>

        <hr>
        
        <Quill name="description" placeholder="Description" label="Description" required={true} bind:value={formData.description} errors={form?.errors}/>
        <Quill name="instructions" placeholder="Instructions" label="Instructions" required={true} bind:value={formData.instructions} errors={form?.errors}/>

      </section>
    </div>

    <br>

    <div class="calyps--card w-full bg-surface-50-950">
      <header class="card-header p-4 bg-surface-200-700-token ">
        <div class="flex justify-between items-center">
          <h3 class="h3">Ingredients</h3>
            <div>
              <button onclick={addIngredient} type="button" class="btn preset-filled-tertiary-500">Add ingredient</button>
            </div>
          </div>
      </header>
      <hr>
      <section class="p-4 space-y-4" bind:this={sortable}>
        {#each formData.ingredients as ingredient, i ({u: ingredient.u})}
        <div>
          {#if !formData.ingredients[i].DELETE}
          <div class="hidden">
            <Field name="sequence"  label="sequence" required={false} type="number" errors={form?.errors?.ingredients?.[i]} bind:value={formData.ingredients[i].sequence} />
          </div>
        
        <section class="flex gap-x-4 gap-y-2 flex-wrap lg:flex-nowrap">
          <div class="flex gap-x-4 w-full">
            <button type="button" class="my-handle outline-none" aria-label="Sort Ingredients">
              <i class="ri-draggable"></i>
            </button>
              <div class="w-full">
                <Field name="name" placeholder="Name" label="Name" required={true} errors={form?.errors?.ingredients?.[i]} bind:value={formData.ingredients[i].name}/>
              </div>
              <div class="">
                <Field name="amount" placeholder="Amount" label="Amount" required={true} errors={form?.errors?.ingredients?.[i]} bind:value={formData.ingredients[i].amount} type="number"/>
              </div>
          </div>
          <div class="flex gap-x-4 items-end">
              <div class="w-full">
                <Field name="unit" placeholder="Unit" label="Unit" required={true} errors={form?.errors?.ingredients?.[i]} bind:value={formData.ingredients[i].unit} choices={unitChoices} type="select"/>
              </div>
              <div class="grow-0">
                  <button type="button" class="btn preset-filled-error-500" onclick={() => removeIngredient(ingredient, i)} aria-label="Delete Ingredient">
                      <i class="ri-delete-bin-2-line"></i>
                  </button>
              </div>
            </div>
        </section>
        {/if}
      </div>
      {/each}
    </section>
    </div>
  </div>

  <div class="calyps--card min-w-64 max-h-fit sticky top-0 bg-surface-50-950">
    <header class="card-header p-4 bg-surface-200-700-token ">
      <h3 class="h3">Visibility</h3>
    </header>
    <hr>
    <section class="p-4 space-y-4">
      <div class="input-group divide-surface-200-800 grid-cols-[1fr_auto] divide-x overflow-visible">
        <Input name="handle" placeholder="handle" label="Handle" required={true} bind:value={formData.handle} errors={form?.errors} />

        <!-- <a class="anchor cursor-pointer p-1" >
          <i class="ri-settings-2-line"></i>
        </a> -->

        <!-- <Tooltip>
         onclick={setHandle()}
          {#snippet _content()}
          <div class="text-sm">
              This is the Recipe Handle. It is how users will navigate to this recipe. Click to Format
          </div>
          {/snippet}
          {#snippet _trigger()}
          <a  class="p-1" onclick={setHandle()}>
            <i class="ri-settings-2-line"></i>
          </a>
          {/snippet}
        </Tooltip> -->

      </div>
      

      <Field name="visibility" placeholder="visibility" label="Visibility" required={true} bind:value={formData.visibility} errors={form?.errors} type="select" 
      choices={visibilityChoices}/>  

      <div class=" flex justify-center">
        <button class="btn preset-filled-secondary-500 w-full" type="submit" >Save</button>
      </div>
    </section>
  </div>
</div>
</form>

<div class="">
<!-- <SuperDebug data={formData} /> -->
</div>