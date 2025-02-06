<script lang="ts">
	// import QuillDisplay from "$components/form/QuillDisplay.svelte";

  import { Segment } from '@skeletonlabs/skeleton-svelte';
  import { page } from '$app/state';
	// import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";
	// import { Ingredient, System, getSystemFromString } from "./Ingredient";
	import Input from "$components/form/Input.svelte";
	// import RecipeTags from "./RecipeTags.svelte";
	import { pluralize } from "$scripts/humanize";
	import WakeLock from "./WakeLock.svelte";
  import Label from '$components/form/Label.svelte';
  import IngredientCheck from './IngredientCheck.svelte';
  import { Ingredient, getSystemFromString} from './Ingredient';
    // import Image from "$components/image/Image.svelte"
    
    // export let recipe: RecipeInterface;

    let {recipe} = $props();

    let system: string = $state("DEFAULT");
    let scalar: string = $state("1");

    let _system = $derived(getSystemFromString(system))
    let ingredients = $derived((recipe.ingredients || []).map(e => Ingredient.asSystem(e, _system, parseFloat(scalar) || 1)))
    // let scalar = $state((Math.max(0, parseFloat(scalar))).toString())

</script>

<div class="relative">
    
    <div class="mx-auto max-w-3xl card">
        <div class="p-4 space-y-4">
            <div class="flex items-center justify-center gap-4 flex-wrap">
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-center">
                    {recipe.name}
                </h1>
                {#if page.data.user?.username === recipe.created_by}
                <div>
                    <a href="/recipe/{recipe._id}/edit" class="btn btn-sm variant-filled-tertiary">
                        <i class="ri-pencil-line"></i> Edit
                    </a>
                </div>
                {/if}
            </div>

            <!-- <RecipeTags tags={recipe.tags} css="justify-center"/> -->

            <!-- <Image image={recipe.image} /> -->

            <div class="flex gap-3 flex-wrap text-center justify-center items-center">
                <div>
                    <Label label="System"/>
                    <Segment bind:value={system}>
                        <Segment.Item value="DEFAULT">Written</Segment.Item>
                        <Segment.Item value="US">US</Segment.Item>
                        <Segment.Item value="Metric">Metric</Segment.Item>
                    </Segment>
                </div>

                <div>
                    <!-- <RadioGroup active="variant-filled-primary" hover="hover:variant-soft-primary" class="input-group-divider" display="flex">
                        
                        <RadioItem bind:group={scalar} name="justify" value={"1"}>1</RadioItem>
                        <RadioItem bind:group={scalar} name="justify" value={"2"}>2</RadioItem>
                        <RadioItem bind:group={scalar} name="justify" value={"3"}>3</RadioItem>
                        <div class="input-group-divider"></div>
                       
                    </RadioGroup> -->
                    <Input bind:value={scalar} type="number" css="p-0 bg-transparent border-none text-center w-10" style="{'min-width: 0 !important;'}"/>
                </div>

                <WakeLock />
                    
            </div>
            
            <div class="flex justify-around">
                <div>Cook Time: {recipe.cook_time} {pluralize(recipe.cook_time, recipe.cook_time)}</div>
                <div>Prep Time: {recipe.prep_time} {pluralize(recipe.prep_time, recipe.prep_time)}</div>
                <div>Servings: {recipe.servings * parseFloat(scalar)}</div>
            </div>

        </div>

        <hr>
        <div class="p-4 space-y-4">


            <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold">Description</h2>
            <!-- <QuillDisplay value={recipe.description}/> -->

            <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold">Ingredients</h2>
            <ul class="list">
            {#each ingredients as ingredient }
                <li>
                    <IngredientCheck name="{ingredient.getAmount()} {ingredient.pluralizeUnit()} {ingredient.name}" /> <!-- {} -->
                </li>
            {/each}
            </ul>

            
            <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold">Instructions</h2>
            <!-- <QuillDisplay value={recipe.instructions}/> -->
        </div>
        
    </div>
</div>