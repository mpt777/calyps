<script>
  import { Switch } from '@skeletonlabs/skeleton-svelte';
  let wakeLock = null;
  let value = $state(false);

  $effect(() => {
    value ? requestWakeLock() : releaseWakeLock();
  })
  const requestWakeLock = async () => {
    try {
      wakeLock = await navigator.wakeLock.request('screen');
    } catch (error) {
      console.error('Failed to acquire wake lock:', error);
    }
  };

  const releaseWakeLock = () => {
    if (value) {
      wakeLock.release();
      wakeLock = null;
    }
  };
</script>

<Switch name="disturb" bind:checked={value}></Switch>