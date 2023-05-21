<template>
    Preview Powered by: Office Online
    <div style="height: 80vh; width: 100%">
      <iframe :src="`https://view.officeapps.live.com/op/view.aspx?src=${url}`" frameborder="0" width="100%" height="100%" ></iframe>
    </div>
</template>

<script setup lang="ts">
defineProps(['url'])
</script>