<script setup lang="ts">
import { NScrollbar, NLayoutSider } from 'naive-ui';
</script>

<template>
    <NScrollbar>
        <NLayoutSider bordered>
            <slot />
        </NLayoutSider>
    </NScrollbar>
</template>