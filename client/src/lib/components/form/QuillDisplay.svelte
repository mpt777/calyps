<script>
  import DOMPurify from 'dompurify';
  let {content} = $props();
  // let safeContent = DOMPurify.sanitize(content);
</script>

<div>{@html content}</div>