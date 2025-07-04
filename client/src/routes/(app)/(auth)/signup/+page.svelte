<script lang="ts">
  let { data, form } = $props();

  import { url } from "$utils/url";
  import { enhance } from '$app/forms';
  import Field from '$components/form/Field.svelte';
  import Message from '$components/message/Message.svelte';

</script>
<form method="POST" use:enhance>
<div class="flex justify-center ">
  
  <div class="calyps--card max-w-sm w-full" >
    <header class="card-header p-4 bg-surface-200-800 ">
      <h2 class="h2">
        Signup
      </h2>
    </header>
    <hr>

    <section class="p-4 space-y-4">
      <Message message={ form?.message } level={form?.level}/>
      <div class="space-y-4">
        <Field name="email" placeholder="Email" label="Email" autocomplete="email" required={true} errors={form?.errors}/>
        <Field name="username" placeholder="Username" label="Username" autocomplete="username" required={true} errors={form?.errors}/>
        
        <Field name="password" placeholder="Password" label="Password" autocomplete="password" required={true} errors={form?.errors} type="password"/>
        <Field name="password1" placeholder="Password" label="Password (Again)" autocomplete="password1" required={true} errors={form?.errors} type="password"/>
      </div>

    </section>
    <hr>
    <footer class="card-footer p-4 space-y-4">
      <div class=" flex justify-center">
        <button class="btn preset-filled-secondary-500 w-full" type="submit" >Signup</button>
      </div>
      
      <div class="flex justify-between">
          <a href="/forgot-password" class="btn preset-tonal border border-surface-500 btn-sm">
              Forgot Password
          </a>
          <a href="/login" class="btn preset-tonal border border-surface-500 btn-sm">
              Login
          </a>
      </div>

    </footer>
  </div>

</div>
</form>