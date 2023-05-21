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

const { options, index, collapsed, name, folderData } = defineProps(['options', 'index', 'collapsed', 'name', 'folderData'])

const onItemSelected = (e: string) => {
    emit('selected', e, index)
}

console.log(folderData)

let size = humaniseSize(calculateFolderSize(folderData))

computed(() => {
    size = humaniseSize(calculateFolderSize(folderData))
})
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
                <template #header-extra>
                    {{ size }}
                </template>
                <template #action>
                </template>
            </NThing>
            <NMenu :options="options" :onUpdate:value="onItemSelected" :collapsed="collapsed" />
        </NLayoutSider>
    </BasePopout>
</template>