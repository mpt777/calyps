<script>
  import BooleanInput from "$components/form/BooleanInput.svelte";
import DurationField from "$components/form/DurationField.svelte";
  import Field from "$components/form/Field.svelte";
    import Quill from "$components/form/Quill.svelte";
  import Message from "$components/message/Message.svelte";

  import SuperDebug from 'sveltekit-superforms';
  import { superForm } from 'sveltekit-superforms/client'


  let {data, form } = $props();

  const { form: formData, errors, constraints, message, enhance } = superForm(data.form, {
    customValidity: true,
    dataType: 'json'
  });

  function addIngredient() {
    console.log(formData)
    $formData.ingredients = $formData.ingredients || [];
    $formData.ingredients.push({
      name: "",
      amount: 0,
      unit: data.units[0].id,
      DELETE:false
    })
    $formData.ingredients = $formData.ingredients;
  }

  async function removeIngredient(item, i) {
      if (item._id){
          $formData.ingredients[i].DELETE=true;
      }
      else {
          $formData.ingredients.splice(i, 1);
      }
      
      $formData.ingredients = $formData.ingredients;
  }


  let visibilityChoices = data.visbilities.map(e => {
    return {"value": e.id, "name": e.name}
  })

  let unitChoices = data.units.map(e => {
    return {"value": e.id, "name": e.name}
  })

</script>

<form method="POST" use:enhance>
  <Message message={ form?.message } level={form?.level}/>

  <div class="flex gap-8 max-w-screen-lg mx-auto flex-wrap md:flex-nowrap ">
    <div class="w-full">
      <div class="calyps--card w-full bg-surface-50-950">
        <header class="card-header p-4 bg-surface-200-700-token ">
          <h2 class="h2">Recipe</h2>
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
        <section class="p-4 space-y-4">
          {#each $formData.ingredients as ingredient, i}
          <section class="flex gap-x-4 gap-y-2 flex-wrap lg:flex-nowrap">
            <div class="flex gap-x-4 w-full">
                <div class="w-full">
                  <Field name="name" placeholder="Name" label="Name" required={true} errors={$errors?.ingredients?.[i]} bind:value={ingredient.name}/>
                </div>
                <div class="">
                  <Field name="amount" placeholder="Amount" label="Amount" required={true} errors={$errors?.ingredients?.[i]} bind:value={ingredient.amount} type="number"/>
                </div>
            </div>
            <div class="flex gap-x-4 items-end">
                <div class="w-full">
                  <Field name="unit" placeholder="Unit" label="Unit" required={true} errors={$errors?.ingredients?.[i]} bind:value={ingredient.unit} choices={unitChoices} type="select"/>
                </div>
                <div class="grow-0">
                    <button type="button" class="btn preset-filled-error-500" onclick={() => removeIngredient(ingredient, i)}>
                        <i class="ri-delete-bin-2-line"></i>
                    </button>
                </div>
            </div>
            
        </section>
        {#if i != $formData.ingredients.length-1}<hr>{/if}
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

<SuperDebug data={formData} />