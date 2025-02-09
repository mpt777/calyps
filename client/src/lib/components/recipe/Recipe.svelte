<script lang="ts">
	// import QuillDisplay from "$components/form/QuillDisplay.svelte";

    import { Segment } from '@skeletonlabs/skeleton-svelte';
    import { page } from '$app/state';
	// import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";
	// import { Ingredient, System, getSystemFromString } from "./Ingredient";
	import Input from "$components/form/Input.svelte";
	// import RecipeTags from "./RecipeTags.svelte";
	import { formatTimeString, pluralize } from "$scripts/humanize";
	import WakeLock from "./WakeLock.svelte";
    import Label from '$components/form/Label.svelte';
    import IngredientCheck from './IngredientCheck.svelte';
    import { Ingredient, getSystemFromString} from './Ingredient';
    import Tooltip from '$components/common/Tooltip.svelte';
    import { url } from '$utils/url';
    import QuillDisplay from '$components/form/QuillDisplay.svelte';
    // import Image from "$components/image/Image.svelte"
    
    // export let recipe: RecipeInterface;

    let {recipe} = $props();

    let system: string = $state("DEFAULT");
    let scalar: string = $state("1");

    let _system = $derived(getSystemFromString(system))
    let ingredients = $derived((recipe.ingredients || []).map(e => Ingredient.asSystem(e, _system, parseFloat(scalar) || 1)))

</script>

<div class="mx-auto max-w-3xl calyps--card border-surface-100-900 bg-surface-50-950">
    <header class="p-4 space-y-4">
        <div class="flex items-center justify-center gap-4 flex-wrap">
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-center">
                {recipe.name}
            </h1>
            {#if page.data.user?.username === recipe.created_by}
            <div>
                <Tooltip>
                    {#snippet _content()}
                    <div class="text-sm">
                        Edit Recipe
                    </div>
                    {/snippet}
                    {#snippet _trigger()}
                    <a href="{url("recipe_edit", {handle:recipe.handle})}" class="btn btn-sm variant-filled-tertiary">
                        <i class="ri-pencil-line text-3xl"></i>
                    </a>
                    {/snippet}
                </Tooltip>
            </div>
            {/if}
            
        </div>
    </header>

    <hr>
    <section class="p-2 space-y-4">
        <!-- <RecipeTags tags={recipe.tags} css="justify-center"/> -->

        <!-- <Image image={recipe.image} /> -->

        <div class="flex gap-3 flex-wrap text-center justify-around items-center">
            <div class="p-1">
                <Label label="System"/>
                <Segment bind:value={system} >
                    <Segment.Item value="DEFAULT" classes={"btn-sm"} >Written</Segment.Item>
                    <Segment.Item value="US" classes={"btn-sm"} >US</Segment.Item>
                    <Segment.Item value="Metric" classes={"btn-sm"} >Metric</Segment.Item>
                </Segment>
            </div>
            
            <div>
                <Label label="Cook Mode"/>
                <WakeLock />
            </div>

            <div>
                <Label label="Servings"/>
                <Segment bind:value={scalar} >
                    <Segment.Item value="1" classes={"btn-sm"} >1</Segment.Item>
                    <Segment.Item value="2" classes={"btn-sm"} >2</Segment.Item>
                    <Segment.Item value="3" classes={"btn-sm"} >3</Segment.Item>
                    <Input bind:value={scalar} type="number" css="p-0 bg-transparent border-none text-center w-10" style="{'min-width: 0 !important;'}"/>
                </Segment>
                
            </div>

        </div>
        
        <div class="flex justify-around">
            <div class="text-center">
                <div class="font-bold">Cook Time:</div>
                <div>{formatTimeString(recipe.cook_time)}</div>
            </div>
            <div class="text-center">
                <div class="font-bold">Prep Time:</div>
                <div>{formatTimeString(recipe.prep_time)}</div>
            </div>
            <div class="text-center">
                <div class="font-bold">Servings:</div>
                <div>{recipe.servings * parseFloat(scalar)}</div>
            </div>
        </div>

    </section>

    <hr>
    <section class="p-4 space-y-16">

        <div class=" space-y-4">
            <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-center">Description</h2>
            <div class="max-w-prose mx-auto"><QuillDisplay content={recipe.description}/></div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="space-y-4">
                <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-center">Ingredients</h2>
                <ul class="list">
                    {#each ingredients as ingredient }
                        <li>
                            <IngredientCheck name="{ingredient.getAmount()} {ingredient.pluralizeUnit()} {ingredient.name}" /> <!-- {} -->
                        </li>
                    {/each}
                </ul>
            </div>

            <div class=" space-y-4">
                <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-center">Instructions</h2>
                <div class="max-w-prose"><QuillDisplay content={recipe.instructions}/></div>
            </div>
        </div>
        
    </section>

</div>