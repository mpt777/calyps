<script>
  import Tooltip from "$components/common/Tooltip.svelte";
import Field from "$components/form/Field.svelte";
  import Quill from "$components/form/Quill.svelte";
import Message from "$components/message/Message.svelte";
    
  import { url } from "$utils/url";

// import SuperDebug from 'sveltekit-superforms';
// import { superForm } from 'sveltekit-superforms/client'


let {data} = $props();

// const { form: formData, errors, constraints, message, enhance } = superForm(data.form, {
//   customValidity: true,
//   dataType: 'json'
// });

function addIngredient() {
  $formData.ingredients = $formData.ingredients || [];
  $formData.ingredients.push({
    name: "",
    amount: 0,
    unit: data.units[0].id,
    sequence: $formData.ingredients.length+1,
    DELETE:false
  })
  $formData.ingredients = $formData.ingredients;
}

async function removeIngredient(item, i) {
    $formData.ingredients[i].DELETE=true;
    $formData.ingredients[i].amount=1;
    $formData.ingredients[i].name="DELETE";
    $formData.ingredients = $formData.ingredients;
}


let visibilityChoices = data.visbilities.map(e => {
  return {"value": e.id, "name": e.name}
})

let unitChoices = data.units.map(e => {
  return {"value": e.id, "name": e.name}
})

  import { reorder, useSortable } from "$scripts/useSortable.svelte";

  let sortable = $state(null);

  useSortable(() => sortable, {
    animation: 200,
    handle: '.my-handle',
    ghostClass: 'opacity-0',
    onEnd(evt) {
        // console.log(items)
        // items = reorder(items, evt);
        // items.forEach((_, i) => {
        //   items[i].sequence = i+1
        // })
        // $formData.ingredients = items;

        // $formData.ingredients = reorder($formData.ingredients, evt);
        // $formData.ingredients.forEach((_, i) => {
        //   $formData.ingredients[i].sequence = i+1
        // })
        // $formData.ingredients = $formData.ingredients;
        // const sequenceInputs = evt.from.querySelectorAll('input[name="sequence"]');
        //   sequenceInputs.forEach((el, idx) => {
        //     console.log(el, idx);  // Check the element and its index
        //     el.value = idx + 1;    // Set the new sequence number

        //     // Dispatch the 'input' event to propagate the change
        //     el.dispatchEvent(new Event('input', { bubbles: true }));
        //   });
        }
  });
</script>


<form method="POST" use:enhance class="space-y-4">
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
            <Field name="name" placeholder="Name" label="Name" required={true} bind:value={$formData.name} errors={$errors}/>
          </div>
          <div class="col-span-12 md:col-span-4">
            <Field name="servings" placeholder="Servings" label="Servings" required={true} bind:value={$formData.servings} errors={$errors} type="number"/>
          </div>
        </div>

        <div class="grid grid-cols-12 md:gap-8">
          <div class="col-span-12 lg:col-span-6">
            <Field name="prep_time"  label="Prep Time" required={true} type="duration" bind:value={$formData.prep_time} errors={$errors}/>

          </div>
          <div class="col-span-12 lg:col-span-6">
            <Field name="cook_time" label="Cook Time" required={true} type="duration" bind:value={$formData.cook_time} errors={$errors}/>
          </div>
        </div>

        <hr>
        
        <Quill name="description" placeholder="Description" label="Description" required={true} bind:value={$formData.description} errors={$errors}/>
        <Quill name="instructions" placeholder="Instructions" label="Instructions" required={true} bind:value={$formData.instructions} errors={$errors}/>

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
        {#each $formData.ingredients as ingredient, i (ingredient)}
        {#if !ingredient.DELETE}
        <div>
        <Field name="sequence"  label="sequence" required={false} type="number" bind:value={$formData.ingredients[i].sequence} errors={$errors?.ingredients?.[i]}/>
        <section class="flex gap-x-4 gap-y-2 flex-wrap lg:flex-nowrap">
          <div class="flex gap-x-4 w-full">
            <button type="button" class="my-handle outline-none">
              <i class="ri-draggable"></i>
            </button>
              <div class="w-full">
                <Field name="name" placeholder="Name" label="Name" required={true} errors={$errors?.ingredients?.[i]} bind:value={$formData.ingredients[i].name}/>
              </div>
              <div class="">
                <Field name="amount" placeholder="Amount" label="Amount" required={true} errors={$errors?.ingredients?.[i]} bind:value={$formData.ingredients[i].amount} type="number"/>
              </div>
          </div>
          <div class="flex gap-x-4 items-end">
              <div class="w-full">
                <Field name="unit" placeholder="Unit" label="Unit" required={true} errors={$errors?.ingredients?.[i]} bind:value={$formData.ingredients[i].unit} choices={unitChoices} type="select"/>
              </div>
              <div class="grow-0">
                  <button type="button" class="btn preset-filled-error-500" onclick={() => removeIngredient(ingredient, i)}>
                      <i class="ri-delete-bin-2-line"></i>
                  </button>
              </div>
          </div>
          
      </section>
      {#if i != $formData.ingredients.length-1}<hr>{/if}
      </div>
      {/if}
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
      <Field name="handle" placeholder="handle" label="Handle" required={true} bind:value={$formData.handle} errors={$errors} />

      <Field name="visibility" placeholder="visibility" label="Visibility" required={true} bind:value={$formData.visibility} errors={$errors} type="select" 
      choices={visibilityChoices}/>  

      <div class=" flex justify-center">
        <button class="btn preset-filled-secondary-500 w-full" type="submit" >Save</button>
      </div>
    </section>
  </div>
</div>
</form>

<!-- {JSON.stringify(items)} -->

<div class="">
<!-- <SuperDebug data={formData} /> -->
</div>