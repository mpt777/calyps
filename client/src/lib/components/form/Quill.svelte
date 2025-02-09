<script>
  import { onMount } from "svelte";
	import Field from "./Field.svelte";

  let editor = null;
  let quill = null;
  let textarea = null;

  let {value = $bindable(""), name= "", label= "", errors={}, required=false, placeholder=""} = $props();

  let requiredClass = required ? "required" : ""; 

  let toolbarOptions = [
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ header: 1 }, { header: 2 }, "blockquote", "link"],
    ["bold", "italic", "underline", "strike"],
    [{ list: "ordered" }, { list: "ordered" }],
    [{ align: [] }],
    ["clean"]
  ];
    
  onMount(async () => {
    const { default: Quill } = await import("quill");
    
    quill = new Quill(editor, {
      modules: {
        toolbar: toolbarOptions
      },
      theme: "snow",
      placeholder: placeholder
    });

    // Set inner HTML to base value
    quill.root.innerHTML = value;

    // On Text change, we need to set the value to the innerHTML
    quill.on('text-change', function(delta, oldDelta, source) {
      value = quill.root.innerHTML;
      textarea.innerHTML = value;
    });
  });

    
</script>
  
<div class="editor-wrapper">
  <label class="label" for="{name}">
    <span class="label-text {requiredClass}">{label}</span>
  </label>
  <div class="ql-wrapper">
    <div bind:this={editor}></div>
  </div>
  <textarea bind:this={textarea} class="opacity-0 h-0 p-0 m-0 flex" required={required} name={name}></textarea>
  {#if errors[name]}
  <p class="text-red-500 text-xs italic mt-3">{errors[name]}</p>
  {/if}
</div>

<style>

</style>