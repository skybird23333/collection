<script setup lang="ts">
import { NAvatar, NButton, NIcon, NThing } from 'naive-ui';
import BasePopout from './BasePopout.vue';
import humaniseSize from '../helpers/humaniseSize'
import { defineProps } from 'vue';

import { DocumentOutline } from "@vicons/ionicons5"

const { data } = defineProps(['data'])

const size = humaniseSize(data.size)

console.log(data)

</script>

<template>
    <BasePopout style="width: 100%;">
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
            <template #action>
                <NButton>Download</NButton>
            </template>
        </NThing>

    </BasePopout>
</template>