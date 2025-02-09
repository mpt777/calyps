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

  let {data, form } = $props();


  let errors=form?.errors;

  // const { form: formData, errors, constraints, message, enhance } = superForm(data.form, {
  //   customValidity: true,
  //   dataType: 'json'
  // });


  let visibilityChoices = data.visbilities.map(e => {
    return {"value": e.id, "name": e.name}
  })

  let unitChoices = data.units.map(e => {
    return {"value": e.id, "name": e.name}
  })

  let myData = $state(data.form)

  let ingredients = $state(form.ingredients)

  ingredients.forEach(e=>{
    e.u=generateUUID();
  })

  let sortable = $state(null);

  useSortable(() => sortable, {
    animation: 200,
    handle: '.my-handle',
    ghostClass: 'opacity-0',
    onEnd(evt) {
      myData.ingredients = reorder(myData.ingredients, evt);
      sortIngredients()
    }
  });

  function sortIngredients() {
    let counter = 1
    myData.ingredients.forEach((_, i) => {
      let value = 0
      if (!myData.ingredients[i].DELETE) {
        value = counter
        counter++
      }
      myData.ingredients[i].sequence = value
    })
    myData.ingredients = [...myData.ingredients]
  }

  function addIngredient() {
    console.log("here")
    myData.ingredients.push({
      name: "",
      amount: 0,
      unit: data.units[0].id,
      sequence: 0,
      u: generateUUID(),
      DELETE:false
    })
    sortIngredients()
    myData.ingredients = myData.ingredients
  }

  async function removeIngredient(item, i) {
    myData.ingredients[i].DELETE=true;
    myData.ingredients[i].amount=1;
    myData.ingredients[i].name="DELETE";
    sortIngredients()
  }
</script>
<pre class="mt-5 w-fit border p-5">{JSON.stringify(myData, null, 2)}</pre>



<form method="POST" use:enhance class="space-y-4">

  <input name="hack" value={JSON.stringify(myData)}>
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
              <a href={url("recipe", {handle: "test"})} class="anchor">
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
            <Field name="name" placeholder="Name" label="Name" required={true} bind:value={form.name} errors={errors}/>
          </div>
          <div class="col-span-12 md:col-span-4">
            <Field name="servings" placeholder="Servings" label="Servings" required={true} bind:value={form.servings} errors={errors} type="number"/>
          </div>
        </div>

        <div class="grid grid-cols-12 md:gap-8">
          <div class="col-span-12 lg:col-span-6">
            <Field name="prep_time"  label="Prep Time" required={true} type="duration" bind:value={form.prep_time} errors={errors}/>

          </div>
          <div class="col-span-12 lg:col-span-6">
            <Field name="cook_time" label="Cook Time" required={true} type="duration" bind:value={form.cook_time} errors={errors}/>
          </div>
        </div>

        <hr>
        
        <Quill name="description" placeholder="Description" label="Description" required={true} bind:value={form.description} errors={errors}/>
        <Quill name="instructions" placeholder="Instructions" label="Instructions" required={true} bind:value={form.instructions} errors={errors}/>

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
        {#each myData.ingredients as ingredient, i ({u: ingredient.u})}
        <div>
          {#if !myData.ingredients[i].DELETE}
        <Field name="sequence"  label="sequence" required={false} type="number" bind:value={myData.ingredients[i].sequence} errors={errors?.ingredients?.[i]}/>
        <section class="flex gap-x-4 gap-y-2 flex-wrap lg:flex-nowrap">
          <div class="flex gap-x-4 w-full">
            <button type="button" class="my-handle outline-none">
              <i class="ri-draggable"></i>
            </button>
              <div class="w-full">
                <Field name="name" placeholder="Name" label="Name" required={true} errors={errors?.ingredients?.[i]} bind:value={myData.ingredients[i].name}/>
              </div>
              <div class="">
                <Field name="amount" placeholder="Amount" label="Amount" required={true} errors={errors?.ingredients?.[i]} bind:value={myData.ingredients[i].amount} type="number"/>
              </div>
          </div>
          <div class="flex gap-x-4 items-end">
              <div class="w-full">
                <Field name="unit" placeholder="Unit" label="Unit" required={true} errors={errors?.ingredients?.[i]} bind:value={myData.ingredients[i].unit} choices={unitChoices} type="select"/>
              </div>
              <div class="grow-0">
                  <button type="button" class="btn preset-filled-error-500" onclick={() => removeIngredient(ingredient, i)}>
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
      <Field name="handle" placeholder="handle" label="Handle" required={true} bind:value={form.handle} errors={errors} />

      <Field name="visibility" placeholder="visibility" label="Visibility" required={true} bind:value={form.visibility} errors={errors} type="select" 
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