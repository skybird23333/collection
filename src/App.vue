<script lang="ts" setup>
import { reactive } from '@vue/reactivity';
import { NConfigProvider, NMenu, NIcon, NSpace, NLayout, NLayoutSider, NScrollbar, NLayoutHeader, NH1, NText, NBreadcrumb, NBreadcrumbItem } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { darkTheme } from 'naive-ui';
import { DocumentOutline, FolderOutline } from "@vicons/ionicons5"
import { h, VNode } from 'vue'
import MenuPopout from './components/MenuPopout.vue';
import FilePopout from './components/FilePopout.vue';
import type { VaultDocument } from './types/interfaces'

interface FolderPopoutData {
  name: string
  type: 'folder',
  data: MenuOption[]
}

interface DocumentPopoutData {
  name: string
  type: 'document',
  data: VaultDocument
}

type PopoutData = FolderPopoutData | DocumentPopoutData

// Our custom type for menu options containing extra data
type FileMenuOption = {
  type: 'folder' | 'document'
  label: string
  key: string
  icon: () => VNode
  data: VaultDocument | any
}


// We will keep a list of popouts here as well as the data they will contain
let state = reactive<{
  popOuts: PopoutData[]
}>({
  popOuts: []
})

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

// Convert the file index tree into menu options format
const indexDataToMenuOptions = (data: any): FileMenuOption[] => {
  return Object.entries(data).map(entry => {
    if (entry[1].name && entry[1].size) { //item is a file
      return {
        label: entry[0],
        key: entry[0],
        icon: renderIcon(DocumentOutline),
        data: entry[1],
        type: 'document'
      }
    } else {
      return {
        label: `${entry[0]}[${Object.keys(entry[1]).length}]`,
        key: entry[0],
        icon: renderIcon(FolderOutline),
        type: 'folder',
        data: entry[1]
      }
    }
  })
}

// Fetch the index data file, and then push the initial
// popout containing the root folder
const fetchIndexData = async () => {
  const res = await fetch('/index.json')
  const data = await res.json()
  state.popOuts.push({
    type: 'folder',
    data: indexDataToMenuOptions(data.resources),
    name: 'collection'
  })
}

// A menu has its active item changed
const onmenuSelected = (option: string, index: number) => {
  //First close all popouts after this menu(if any)
  state.popOuts.splice(index + 1)

  const optionData: MenuOption = (state.popOuts[index] as FolderPopoutData).data
    .find(d => d.key == option)

  if (!optionData) return

  if (optionData.type == 'folder') {
    state.popOuts.push({
      type: 'folder',
      data: indexDataToMenuOptions(optionData.data),
      name: optionData.label
    })
  } else if (optionData.type == 'document') {
    state.popOuts.push({
      type: 'document',
      data: optionData.data,
      name: optionData.data.name
    })
  }
}

fetchIndexData()

</script>

<template>
  <NConfigProvider :theme="darkTheme">
    <NSpace vertical style="gap: none;">

      <NLayoutHeader style="padding: 5px; height: 8vh;" bordered>
        <NText style="font-size: x-large;">
          WACE-VAULT
        </NText>

        <NBreadcrumb>
          <NBreadcrumbItem v-for="[index, popout] in state.popOuts.entries()" :key="index" :clickable="false">
            <NIcon>
              <FolderOutline v-if="popout.type === 'folder'"/>
              <DocumentOutline v-if="popout.type === 'document'" />
            </NIcon>
            {{ popout.name }}
          </NBreadcrumbItem>
        </NBreadcrumb>
      </NLayoutHeader>


      <NScrollbar :x-scrollable="true">

        <NLayout has-sider>
          
          <div v-for="[index, popout] in state.popOuts.entries()" :key="index">
            <MenuPopout v-if="popout.type == 'folder'" :options="popout.data" :index="index" @selected="onmenuSelected"
            :collapsed="(state.popOuts.length - index > 2)" />
            <FilePopout v-if="popout.type == 'document'" :data="popout.data" :index="index" />
          </div>
          
          <NLayout>
            
          </NLayout>
          
        </NLayout>

      </NScrollbar>
    </NSpace>
  </NConfigProvider>
</template>

<style scoped></style>
