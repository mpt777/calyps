<script>
  import BooleanInput from "$components/form/BooleanInput.svelte";
import DurationField from "$components/form/DurationField.svelte";
  import Field from "$components/form/Field.svelte";
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
      unit: "",
      DELETE:false
    })
    $formData.ingredients = $formData.ingredients;
  }

</script>

<form method="POST" use:enhance>
  <Message message={ form?.message } level={form?.level}/>
  <div class="space-y-4">
  <Field name="name" placeholder="Name" label="Name" required={true} errors={$errors}/>
  <Field name="handle" placeholder="handle" label="Handle" required={true} errors={$errors} />

  <Field name="description" placeholder="description" label="description" required={true} errors={$errors}/>
  <Field name="instructions" placeholder="instructions" label="instructions" required={true} errors={$errors}/>

  <Field name="prep_time" placeholder="prep_time" label="prep_time" required={true} type="duration" errors={$errors}/>
  <Field name="cook_time" placeholder="cook_time" label="cook_time" required={true} type="duration" errors={$errors}/>

  <Field name="servings" placeholder="servings" label="servings" required={true} errors={$errors}/>

  <Field name="visibility" placeholder="visibility" label="visibility" required={true} errors={$errors}/>  
  </div>

  <button onclick={addIngredient} type="button">Add ingredient</button>

  {#each $formData.ingredients as ingredient, i}
    <div class="space-y-4">
      <Field name="name" placeholder="Name" label="Name" required={true} errors={$errors} value={ingredient.name}/>
      <Field name="amount" placeholder="Amount" label="Amount" required={true} errors={$errors} value={ingredient.amount} type="number"/>
      <Field name="unit" placeholder="Unit" label="Unit" required={true} errors={$errors} value={ingredient.unit} />
      <Field errors={$errors}>
        {#snippet input()}
          <BooleanInput name="DELETE" label="Delete" bind:value={ingredient.DELETE}/>
        {/snippet}
      </Field>
    </div>
  {/each}

  <div class=" flex justify-center">
  <button class="btn preset-filled-secondary-500 w-full" type="submit" >Save</button>
  </div>
</form>

<SuperDebug data={formData} />