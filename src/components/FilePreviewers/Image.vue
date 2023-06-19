<template>
    Resolved Document Type: Image
    <img :src="props.url">
</template>

<script setup lang="ts">
const props = defineProps(['url'])

</script>