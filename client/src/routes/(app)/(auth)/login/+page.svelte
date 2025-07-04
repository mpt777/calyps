<script lang="ts">
    let { data, form } = $props();

    import { enhance } from '$app/forms';
    import Field from '$components/form/Field.svelte';
    import Input from '$components/form/Input.svelte';
    import Password from '$components/form/Password.svelte';
    import Message from '$components/message/Message.svelte';
    import { url } from '$utils/url.js';

</script>
<form method="POST" use:enhance>
	<div class="flex justify-center ">
		
		<div class="calyps--card max-w-sm w-full" >
			<header class="card-header p-4 bg-surface-200-800 ">
				<h2 class="h2">
					Login
				</h2>
			</header>
			<hr>

			<section class="p-4 space-y-4">
				<Message message={ form?.message } level={form?.level}/>
				<div class="space-y-4">
					<Field name="username" placeholder="Username" label="Username" autocomplete="username" required={true}/>

					<Password></Password>

				</div>

			</section>
			<hr>
			<footer class="card-footer p-4 space-y-4">
				<div class=" flex justify-center">
					<button class="btn preset-filled-secondary-500 w-full" type="submit" >Login</button>
				</div>
				
				<div class="flex justify-between">
						<a href="/auth/forgot-password" class="btn preset-tonal border border-surface-500 btn-sm">
								Forgot Password
						</a>
						<a href="{url("signup")}" class="btn preset-tonal border border-surface-500 btn-sm">
								Sign Up
						</a>
				</div>

			</footer>
		</div>

	</div>
</form>