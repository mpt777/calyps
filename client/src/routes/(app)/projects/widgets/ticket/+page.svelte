<script>
  let trains = [
    { "name": 1, "value": 1, "count": 0 },
    { "name": 2, "value": 2, "count": 0 },
    { "name": 3, "value": 4, "count": 0 },
    { "name": 4, "value": 7, "count": 0 },
    { "name": 5, "value": 10, "count": 0 },
    { "name": 6, "value": 15, "count": 0 }
  ];

  let result = 0; // Initialize result

  function calculate() {
    result = 0; // Reset result before calculating
    trains.forEach(e => {
      result += (e.value * e.count);
    });
  }
</script>

<div class="flex justify-center">
	<div class="calyps--card">
		<header class="card-header p-4 bg-surface-200-800 ">
			<h2 class="h2">
				Ticket to Ride Calculator
			</h2>
		</header>
		<hr>
		
		<section class="p-4">Enter the number of segments based on their length down below..</section>
		<section class="p-4 space-y-4">
			{#each trains as train}
			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<div class="ig-cell preset-tonal-surface">{train.name} Segment</div>
				<input type="number" class="ig-input input--min-w-4" min=0 value={train.count}/>

				<div class="input-group-shim p-0!">
					<div class="flex p-0! h-full">
						<button type="button" class="btn h-full preset-filled-warning-500 rounded-none cursor-pointer" onclick={() => train.count = Math.max(train.count-1, 0)} aria-label="Remove Segment">-</button>
						<button type="button" class="btn h-full preset-filled-tertiary-500 rounded-none cursor-pointer"  onclick={() => train.count++} aria-label="Add Segment">+</button>
					</div>
				</div>
			</div>
			{/each}

			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<button type="button" class="btn btn-lg h-full preset-filled-primary-500 rounded-none cursor-pointer" onclick={calculate} aria-label="Calculate Results">
					<i class="ri-calculator-line"></i> Results 
				</button>
				<button>{result}</button>
			</div>

		</section>
		<hr>
		<footer class="card-footer p-4 flex justify-between">
			<div>
			</div>
				<a href="/projects" class="btn preset-tonal border border-surface-500 float-right"><i class="ri-arrow-left-line"></i> Return</a>
		</footer>
	</div>
</div>