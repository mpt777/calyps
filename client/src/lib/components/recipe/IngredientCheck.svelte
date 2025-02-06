<script>
  let {name} = $props();
  let checked = $state(false);
</script>

<div class="flex items-center space-x-2"> 
  
  <input class="checkbox" type="checkbox" bind:checked={checked} name="{name}"/>
  <label class="{checked ? 'line-through' : ''}" for="{name}">{name}</label>
</div>