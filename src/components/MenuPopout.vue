<script setup lang="ts">
import { NAvatar, NButton, NIcon, NLayoutSider, NMenu, NThing } from 'naive-ui';
import BasePopout from './BasePopout.vue';
import { onUpdated, computed } from 'vue';
import { FolderOutline } from '@vicons/ionicons5';
import calculateFolderSize from '../helpers/calculateFolderSize'
import humaniseSize from '../helpers/humaniseSize';

const emit = defineEmits<{
    (event: 'selected', option: string, index: number): void
}>
    ()

const props = defineProps(['options', 'index', 'collapsed', 'name', 'folderData'])

const onItemSelected = (e: string) => {
    emit('selected', e, props.index)
}

const size = computed(() => humaniseSize(calculateFolderSize(props.folderData)))
//FIXME: Folder size doesn't get updated when opening a different folder


</script>

<template>
    <BasePopout>
        <NLayoutSider collapse-mode="width" :collapsed="collapsed" :collapsedWidth="48" style="min-height: 94vh" bordered>
            <NThing v-if="!collapsed" style="padding: 15px;">
                <template #avatar>
                    <NAvatar>
                        <NIcon>
                            <FolderOutline></FolderOutline>
                        </NIcon>
                    </NAvatar>
                </template>
                <template #header>
                    {{ name }}
                </template>
                <template #description>
                    {{ size }}
                </template>
                <template #action>
                </template>
            </NThing>
            <NMenu :options="options" :onUpdate:value="onItemSelected" :collapsed="collapsed" />
        </NLayoutSider>
    </BasePopout>
</template>