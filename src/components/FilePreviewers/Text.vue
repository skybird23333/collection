<template>
    Resolved Document Type: Text
    <NCode :code="text.value">
        
    </NCode>
</template>

<script setup lang="ts">
import { NCode } from 'naive-ui';
import { reactive } from 'vue'
const props = defineProps(['url'])
const text = reactive({value: 'Text'})
const fetchText = async () => {
    const res = await fetch('https://github.com/wace-vault/collection/raw/main/resources/_miscellaneous/doe%20link.txt', {redirect: 'follow'})
    text.value = await res.text()
}

fetchText()

</script>