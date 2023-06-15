<script setup lang="ts">
import { NAvatar, NButton, NIcon, NThing } from 'naive-ui';
import BasePopout from './BasePopout.vue';
import humaniseSize from '../helpers/humaniseSize'
import { computed, reactive } from 'vue'

import { DocumentOutline } from "@vicons/ionicons5"
import FilePreviewer from './FilePreviewer.vue';

const props = defineProps(['data'])

const size = computed(() => humaniseSize(props.data.size))

const downloadFile = () => {
    location.href = props.data.url
}
</script>

<template>
    <BasePopout style="width: 100%">
        <NThing style=" padding: 20px;">
            <template #avatar>
                <NAvatar>
                    <NIcon>
                        <DocumentOutline />
                    </NIcon>
                </NAvatar>
            </template>
            <template #header>
                {{ data?.name }}
            </template>
            <template #description>
                {{ size }}
            </template>
            <template #header-extra>
                <NButton
                    @click="downloadFile"
                >Download</NButton>
            </template>
            <FilePreviewer :url="props.data.url"></FilePreviewer>
        </NThing>
    </BasePopout>
</template>