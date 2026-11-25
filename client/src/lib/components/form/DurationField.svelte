<script>
  let hours = $state(0);
  let minutes = $state(0);
  let {value = $bindable(), name} = $props();

  hours = Math.floor(value / 3600);
  minutes = Math.floor((value % 3600) / 60);

  $effect(() => {
    value = hours * 3600 + minutes * 60;
  });
</script>

<div class="flex">
  <input name="{name}" value={value} class="hidden">
  <div class="field-group divide-surface-200-800 flex divide-x flex-wrap lg:flex-nowrap">
    <div class="flex w-full">
      <div class="label label-text preset-tonal min-w-fit">Hours</div>
      <input type="number" class="input input--min-w-4 divide-x w-full" min="0" bind:value={hours} />
    </div>

    <div class="flex w-full border-t-2 lg:border-t-0">
      <div class="label label-text preset-tonal min-w-fit">Minutes</div>
      <input type="number" class="input input--min-w-4 divide-x w-full " min="0" bind:value={minutes} />
    </div>
  </div>
</div>