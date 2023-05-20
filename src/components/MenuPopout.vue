<script setup lang="ts">
import { NLayoutSider, NMenu } from 'naive-ui';
import BasePopout from './BasePopout.vue';
import { defineProps, defineEmits } from 'vue';

const emit = defineEmits<{
    (event: 'selected', option: string, index: number): void
}>
()

const { options, index, collapsed } = defineProps(['options', 'index', 'collapsed'])

const onItemSelected = (e: string) => {
    emit('selected', e, index)
}


</script>

<template>
    <BasePopout>
        <NLayoutSider
            collapse-mode="width"
            :collapsed="collapsed"
            :collapsedWidth="48"
            style="min-height: 94vh"
            bordered
        >
            <NMenu :options="options" :onUpdate:value="onItemSelected" :collapsed="collapsed"/>
        </NLayoutSider>
    </BasePopout>
</template>