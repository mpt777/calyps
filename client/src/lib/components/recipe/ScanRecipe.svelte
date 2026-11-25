<script>
  import { ingredientsMissingUnit } from "./scanDraft";

  // Upload a photo of a recipe card; calls onDraft(draft) with what the
  // server read. Nothing is saved until the user submits the recipe form.
  /** @type {{ onDraft: (draft: import("./scanDraft").RecipeDraft) => void }} */
  let { onDraft } = $props();

  // The server downsizes to this anyway; shrinking first keeps uploads small
  // on phones and under the SvelteKit body size limit.
  const MAX_SIDE = 2000;

  /** @type {HTMLInputElement | null} */
  let fileInput = $state(null);
  let status = $state("idle"); // idle | reading | done | error
  let message = $state("");
  let rawText = $state("");

  /** @param {File} file */
  async function shrink(file) {
    try {
      const bitmap = await createImageBitmap(file, { imageOrientation: "from-image" });
      const scale = Math.min(1, MAX_SIDE / Math.max(bitmap.width, bitmap.height));
      if (scale === 1 && file.size < 2 * 1024 * 1024) return file;
      const canvas = document.createElement("canvas");
      canvas.width = Math.round(bitmap.width * scale);
      canvas.height = Math.round(bitmap.height * scale);
      canvas.getContext("2d")?.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
      /** @type {Blob | null} */
      const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.9));
      return blob ? new File([blob], "recipe-card.jpg", { type: "image/jpeg" }) : file;
    } catch {
      // The browser can't decode it (e.g. HEIC outside Safari): send as-is.
      return file;
    }
  }

  /** @param {Event & { currentTarget: HTMLInputElement }} event */
  async function scan(event) {
    const file = event.currentTarget.files?.[0];
    if (!file) return;

    status = "reading";
    message = "";
    rawText = "";
    try {
      const body = new FormData();
      body.append("image", await shrink(file));
      const response = await fetch("/recipe/r/add/scan", { method: "POST", body });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.message || "Something went wrong reading that photo.");

      const draft = data.draft;
      rawText = draft.raw_text || "";
      if (!rawText) throw new Error("No text was found in that photo. Try a closer, well-lit shot.");

      onDraft(draft);
      status = "done";
      /** @param {number} n @param {string} word */
      const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;
      const missing = ingredientsMissingUnit(draft);
      message =
        `Filled in ${plural(draft.ingredients.length, "ingredient")} and ${plural(draft.instructions.length, "step")}. ` +
        (missing ? `${plural(missing, "ingredient")} had no unit we recognise, so pick ${missing === 1 ? "it" : "them"} below. ` : "") +
        "Check everything before saving.";
    } catch (error) {
      status = "error";
      message = error instanceof Error ? error.message : "Something went wrong reading that photo.";
    } finally {
      if (fileInput) fileInput.value = "";
    }
  }
</script>

<div class="calyps--card w-full bg-surface-50-950 max-w-(--breakpoint-lg) mx-auto mb-8">
  <section class="p-4 flex flex-col md:flex-row md:items-center gap-4">
    <div class="grow">
      <h3 class="h4">Start from a recipe card</h3>
      <p class="text-sm opacity-75">Take or upload a photo and we'll fill in the form below for you to review.</p>
    </div>
    <label class="btn preset-filled-primary-500 cursor-pointer {status === 'reading' ? 'opacity-50 pointer-events-none' : ''}">
      {#if status === "reading"}
        <i class="ri-loader-4-line animate-spin"></i> Reading card…
      {:else}
        <i class="ri-camera-line"></i> Scan a card
      {/if}
      <input
        bind:this={fileInput}
        type="file"
        accept="image/*"
        class="hidden"
        disabled={status === "reading"}
        onchange={scan}
      />
    </label>
  </section>

  {#if message}
    <section class="px-4 pb-4">
      <p class="text-sm {status === 'error' ? 'text-error-500' : 'text-success-700-300'}">{message}</p>
      {#if rawText}
        <details class="mt-2 text-sm">
          <summary class="cursor-pointer opacity-75">Text read from the card</summary>
          <pre class="mt-2 p-2 whitespace-pre-wrap bg-surface-100-900 rounded-base">{rawText}</pre>
        </details>
      {/if}
    </section>
  {/if}
</div>
