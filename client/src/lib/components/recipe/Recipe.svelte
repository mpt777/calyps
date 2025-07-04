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
                    
                    <a href="{url("recipe_edit", {handle:recipe?.handle})}" class="btn btn-sm preset-filled-tertiary-500">
                    <!-- <a href="/recipe/{recipe.handle}/edit" class="btn btn-sm variant-filled-tertiary" aria-label="Edit Recipe"> -->
                        <i class="ri-pencil-line text-3xl"></i>
                    </a>
                    {/snippet}
                </Tooltip>
            </div>
            {/if}
            
        </div>
    </header>

    {#if recipe.tag_types}
    <section class="p-4 pt-0">
      <div class="flex items-center  justify-center gap-1">
        {#each recipe.tag_types as tag_type}
        <div class="chip preset-filled ">{tag_type}</div>
        {/each}
      </div>
    </section>
    
    {/if}
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
            
            <div >
                <Label label="Cook Mode"/>
                <div><WakeLock /></div>
                <span class="text-xs">Prevents Screen Sleep</span>
            </div>

            <div>
                <Label label="Servings"/>
                <Segment bind:value={scalar} >
                    <Segment.Item value="1" classes={"btn-sm"} >1</Segment.Item>
                    <Segment.Item value="2" classes={"btn-sm"} >2</Segment.Item>
                    <Segment.Item value="3" classes={"btn-sm"} >3</Segment.Item>
                    <Input bind:value={scalar} type="number" css="p-0 bg-transparent border-none text-center w-10"/>
                </Segment>
                
            </div>

        </div>
        
        <div class="flex justify-around gap-1">
            <div class="text-center w-full">
                <i class="ri-time-line"></i> Cook Time: 
                <span class="font-bold text-nowrap">{formatTimeString(recipe.cook_time)}</span>
            </div>
            <div class="text-center w-full">
                <i class="ri-time-line-fill"></i> Prep Time:
                <span class="font-bold text-nowrap">{formatTimeString(recipe.prep_time)}</span>
            </div>
            <div class="text-center w-full">
                <i class="ri-group-line"></i> Servings:
                <span class="font-bold text-nowrap">{recipe.servings * parseFloat(scalar)}</span>
            </div>
        </div>

    </section>

    <hr>
    <section class="p-8 space-y-8">

        <div class=" space-y-4">
            <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-center">Description</h2>
            <div class="max-w-prose mx-auto"><QuillDisplay content={recipe.description}/></div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
            <div class=" space-y-4">
                <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-center">Ingredients</h2>
                <ul class="list space-y-1">
                    {#each ingredients as ingredient }
                        <li class="">
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