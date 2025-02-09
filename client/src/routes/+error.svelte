<script>
  import { page } from '$app/state';
</script>
here
<h1>{page.status}: {page?.error?.message}</h1>