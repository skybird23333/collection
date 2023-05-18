<script lang="ts">
import { NMenu } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { defineComponent } from 'vue'

const menuOptions: MenuOption[] = [
  {
    label: 'Label',
    key: 'key',
  },
]

let activeKey = "a"

export default defineComponent({
  setup() {
    return {
      menuOptions
    }
  },
  components: {
    NMenu
  }
}) 
</script>

<template>
  <n-menu :options="menuOptions" />
</template>

<style scoped>
</style>
