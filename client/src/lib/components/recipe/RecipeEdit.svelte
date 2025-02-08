<script>
    import DurationField from "$components/form/DurationField.svelte";
    import Field from "$components/form/Field.svelte";
    import Message from "$components/message/Message.svelte";

    import { superForm } from 'sveltekit-superforms';

    import { recipeSchema } from '$lib/forms/recipe';

    let {data} = $props();

    const { form } = superForm(data.form);

</script>

<Message message={ form?.message } level={form?.level}/>
<div class="space-y-4">
  <Field name="name" placeholder="Name" label="Name" required={true} form={form}/>
  <Field name="handle" placeholder="handle" label="Handle" required={true} form={form}/>

  <Field name="description" placeholder="description" label="description" required={true} form={form}/>
  <Field name="instructions" placeholder="instructions" label="instructions" required={true} form={form}/>

  <Field name="prep_time" placeholder="prep_time" label="prep_time" required={true} type="duration" form={form}/>
  <Field name="cook_time" placeholder="cook_time" label="cook_time" required={true} type="duration" form={form}/>

  <Field name="servings" placeholder="servings" label="servings" required={true} form={form}/>

  <Field name="visibility" placeholder="visibility" label="visibility" required={true} form={form}/>  
</div>

<div class="space-y-4">
  <Field name="name" placeholder="Name" label="Name" required={true} form={form}/>
  <Field name="amount" placeholder="Amount" label="Amount" required={true} form={form}/>
  <Field name="unit" placeholder="Unit" label="Unit" required={true} form={form}/>
  <Field name="DELETE" placeholder="Delete" label="Delete" required={true} form={form}/>
</div>

<div class=" flex justify-center">
  <button class="btn preset-filled-secondary-500 w-full" type="submit" >Save</button>
</div>