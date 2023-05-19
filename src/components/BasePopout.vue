<script setup lang="ts">
import { NScrollbar, NLayoutSider } from 'naive-ui';
</script>

<template>
    <NScrollbar style="height: 94vh;">
        <NLayoutSider bordered style="min-height: 94vh;">
            <slot />
        </NLayoutSider>
    </NScrollbar>
</template>

<style scoped>
</style>