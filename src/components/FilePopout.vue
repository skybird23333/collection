<script setup lang="ts">
import { NAvatar, NButton, NIcon, NThing } from 'naive-ui';
import BasePopout from './BasePopout.vue';
import humaniseSize from '../helpers/humaniseSize'
import { computed, reactive } from 'vue'

import { DocumentOutline } from "@vicons/ionicons5"
import FilePreviewer from './FilePreviewer.vue';

const props = defineProps(['data'])

const size = computed(() => humaniseSize(props.data.size))

//Github will send the file back in a format that makes
// it get downloaded instead of being rendered.
const objectDownloadURL = reactive({ url: '' })

const downloadFile = () => {
    objectDownloadURL.url = props.data.url
    objectDownloadURL.url = ''
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

        <object
            :data="objectDownloadURL.url"
            style="display: none"
        ></object>

    </BasePopout>
</template>