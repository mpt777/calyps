<script>
  import DOMPurify from 'dompurify';
  let {content} = $props();
  // let safeContent = DOMPurify.sanitize(content);
</script>

<div class=" ql-container ql-snow border-none!">
  <div class="ql-editor p-0! ">{@html content}</div>
</div>