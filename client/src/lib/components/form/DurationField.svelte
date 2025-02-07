<script>
  import Input from "./Input.svelte";

  let hours = $state(0);
  let minutes = $state(0);
  let {value = $bindable(), name} = $props();

  $effect(() => {
    value = hours * 3600 + minutes * 60;
  });
</script>

<div class="flex gap-4">
  <input name="{name}" value={value} class="hidden">
  <div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
    <div class="input-group-cell preset-tonal-surface">Hours</div>
    <input type="number" class="input--min-w-4 divide-x" min="0" bind:value={hours} />
  </div>
  <div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
    <div class="input-group-cell preset-tonal-surface">Minutes</div>
    <input type="number" class="input--min-w-4 divide-x" min="0" bind:value={minutes} />
  </div>
</div>