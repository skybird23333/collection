
<template>
    <component :is="fileViewerStrategy()" :url="url"></component>
</template>

<script setup lang="ts">
import Markdown from './FilePreviewers/Markdown.vue';
import Office from './FilePreviewers/Office.vue';
import PDF from './FilePreviewers/PDF.vue';
import Text from './FilePreviewers/Text.vue'
import None from './FilePreviewers/None.vue'
import Image from './FilePreviewers/Image.vue'

const props = defineProps({
    url: {
        type: String,
        required: true
    }
})

const fileViewerStrategy = () => {
    const extension = props.url.split('.')[props.url.split('.').length - 1]
    switch (extension) {
        case 'pdf':
            return PDF
        case 'xls':
        case 'xlsx':
        case 'doc':
        case 'docx':
        case 'ppt':
        case 'pptx':
        //All the office extensions. I think.
            return Office
        case 'md':
            return Markdown
        case 'exe':
            return None
        case 'png':
        case 'jpg':
        case 'webp':
            return Image
        default:
            return Text
    }
}

</script>