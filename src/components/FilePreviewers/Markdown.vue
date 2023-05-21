<template>
    Resolved Document Type: MD
    <div v-html="compiledMarkdown"></div>
</template>

<script setup lang="ts">
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { computed, reactive } from 'vue'
const props = defineProps(['url'])
const text = reactive({value: 'Text'})
const fetchDocument = async () => {
    const res = await fetch(props.url, {redirect: 'follow'})
    text.value = await res.text()
}
fetchDocument()
const compiledMarkdown = computed(() => {
  return DOMPurify.sanitize(marked.parse(text.value))
})
</script>