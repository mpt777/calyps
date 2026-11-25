<script>
  import { Switch } from '@skeletonlabs/skeleton-svelte';
  let wakeLock = null;
  let value = $state(false);
  let {label} = $props();

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

	<Switch {value} onCheckedChange={(e) => (value = e.checked)}>
		<Switch.Control>
			<Switch.Thumb />
		</Switch.Control>
		<Switch.Label>{label}</Switch.Label>
		<Switch.HiddenInput />
	</Switch>
<!-- <Switch name="disturb" checked={value} onCheckedChange={(e) => (value = e.checked)}></Switch> -->