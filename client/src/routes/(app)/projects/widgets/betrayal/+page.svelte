<script>
	let diceCount = $state(0);
	let interest = $state(0);
	let result = $state(0.0);

	let probabilityType = $state('2');

	const simulations = 50000;

	function calculate() {
		let total_list = []
		for(var i=0; i < simulations; i++) {
			let total = 0
			for(var j = 0; j < diceCount; j++)
			{
				total += Math.floor(Math.random() * 3);
			}
			total_list.push(total)
		}  

		const BiggerElements = (value) => (element) => element > value;
		const SmallerElements = (value) => (element) => element < value;
		const SameElements = (value) => (element) => element === value;

		switch (probabilityType) {
			case "0":
				result = 1- total_list.filter(SmallerElements(interest)).length / total_list.length;
				break;
			
			case "1":
				result = (total_list.filter(BiggerElements(interest)).length / total_list.length);
				break;
			
			case "2":
				result = total_list.filter(SameElements(interest)).length / total_list.length;
				break;
			
			case "3":
				result = total_list.filter(SmallerElements(interest)).length / total_list.length;
				break;
			
			case "4":
				result = 1 - (total_list.filter(BiggerElements(interest)).length / total_list.length);
				break;
			
			default:
				console.error("Invalid probability type");
				return;
		}

	}

</script>
<div class="flex justify-center">
	<div class="calyps--card">
		<header class="card-header p-4 bg-surface-200-700 ">
			<h2 class="h2">
				Betrayal Probability Calculator 
			</h2>
		</header>
		<hr>
		
		<section class="p-4">Select the number of dice in play, the value of interest, and the type of probability.</section>
		<section class="p-4 space-y-4">

			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<div class="input-group-cell preset-tonal-surface">Dice Rolled</div>
				<input type="number" class="input--min-w-4" min=0 value="{diceCount}"/>

				<div class="input-group-shim p-0!">
					<div class="flex p-0! h-full">
						<a class="btn h-full preset-filled-warning-500 rounded-none cursor-pointer" onclick={() => diceCount = Math.max(diceCount-1, 0)}>-</a>
						<a class="btn h-full preset-filled-tertiary-500 rounded-none cursor-pointer" onclick={() => diceCount++}>+</a>
					</div>
				</div>
			</div>

			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<div class="input-group-cell preset-tonal-surface">Value of Interest</div>
				<input type="number" class="input--min-w-4 divide-x" min=0 value="{interest}"/>

				<div class="input-group-shim p-0!">
					<div class="flex p-0! h-full">
						<a class="btn h-full preset-filled-warning-500 rounded-none cursor-pointer" onclick={() => interest = Math.max(interest-1, 0)}>-</a>
						<a class="btn h-full preset-filled-tertiary-500 rounded-none cursor-pointer" onclick={() => interest++}>+</a>
					</div>
				</div>
			</div>

			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<div class="input-group-cell preset-tonal-surface divide-x">Probability</div>

				<select class="select rounded-none" bind:value={probabilityType}>
					<option value="0">Greater Than or Equal</option>
					<option value="1">Greater Than</option>
					<option value="2">Equal</option>
					<option value="3">Less Than</option>
					<option value="4">Less Than or Equal</option>
				</select>

			</div>

			<div class="input-group divide-surface-200-800 grid-cols-[auto_1fr_auto] divide-x">
				<a class="btn btn-lg h-full preset-filled-primary-500 rounded-none cursor-pointer" onclick={calculate} aria-label="Calculate">
					<i class="ri-calculator-line"></i> Results 
				</a>
				<button>{result.toFixed(4)}</button>
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