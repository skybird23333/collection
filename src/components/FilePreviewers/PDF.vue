<template>
    Preview Powered by: Google Drive
    <div style="height: 80vh; width: 100%">
      <iframe :src="`https://drive.google.com/viewerng/
viewer?embedded=true&url=${url}`" frameborder="0" width="100%" height="100%" ></iframe>
    </div>
</template>

<script setup lang="ts">
defineProps(['url'])
</script>