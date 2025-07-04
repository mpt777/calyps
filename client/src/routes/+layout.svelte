<script lang="ts">
     // Finally, your application's global stylesheet (sometimes labeled 'app.css')
    import "../app.css"
    

	// import { initializeStores } from '@skeletonlabs/skeleton';

    // import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
    // import { storePopup } from '@skeletonlabs/skeleton';
    // storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	// initializeStores();

    let {children} = $props();

    import { Toaster } from '@skeletonlabs/skeleton-svelte';
    import { toaster } from '../lib/toaster-svelte';
  </script>
  
<Toaster {toaster}></Toaster>


{@render children()}