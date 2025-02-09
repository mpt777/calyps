<script>
  import { page } from '$app/state';
</script>

<div class="flex justify-center ">
		
  <div class="calyps--card max-w-sm w-full " >
    <header class="card-header p-4 preset-tonal-error tonal">
      <h2 class="h2">
        {page.status}: {page?.error?.message}
      </h2>
    </header>
    <hr>

    <section class="p-4 space-y-4 text-center">
        <div>Sorry about that!</div>
        <a href="/" class="btn btn-lg h-full preset-filled-secondary-500 ">Return Home</a>
    </section>
  </div>

</div>