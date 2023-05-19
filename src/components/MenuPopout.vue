<script setup lang="ts">
import { NMenu } from 'naive-ui';
import BasePopout from './BasePopout.vue';
import { defineProps, defineEmits } from 'vue';

const emit = defineEmits<{
    (event: 'selected', option: string, index: number): void
}>
()

const { options, index } = defineProps(['options', 'index'])

const onItemSelected = (e: string) => {
    emit('selected', e, index)
}

</script>

<template>
    <BasePopout>
        <NMenu :options="options" :onUpdate:value="onItemSelected"/>
    </BasePopout>
</template>