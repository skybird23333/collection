<script lang="ts" setup>
import { reactive } from '@vue/reactivity';
import { NConfigProvider, NMenu, NIcon, NSpace, NLayout, NLayoutSider, NScrollbar, NLayoutHeader, NH1, NText } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { darkTheme } from 'naive-ui';
import { DocumentOutline, FolderOutline } from "@vicons/ionicons5"
import { h } from 'vue'
import MenuPopout from './components/MenuPopout.vue';
import FilePopout from './components/FilePopout.vue';

interface FolderPopoutData {
    type: 'folder',
    data: MenuOption[]
}

interface DocumentPopoutData {
    type: 'document',
    data: VaultDocument
  }

type PopoutData = FolderPopoutData | DocumentPopoutData

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
const indexDataToMenuOptions = (data: any): MenuOption[] => {
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
        label: entry[0],
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
    data: indexDataToMenuOptions(data.resources)
  })
}

// A menu has its active item changed
const onmenuSelected = (option: string, index: number) => {
  //First close all popouts after this menu(if any)
  state.popOuts.splice(index + 1)

  const optionData = (state.popOuts[index] as FolderPopoutData).data
                      .find(d => d.key == option)

  if(!optionData) return

  console.log(optionData)
  
  if(optionData.type == 'folder') {
    state.popOuts.push({
      type: 'folder',
      data: indexDataToMenuOptions(optionData.data)
    })
  } else if(optionData.type == 'document') {
    state.popOuts.push({
      type: 'document',
      data: optionData.data
    })
  }
}

fetchIndexData()

</script>

<template>
  <NConfigProvider :theme="darkTheme">
    <NSpace vertical style="gap: none;">

      <NLayoutHeader style="padding: 5px; height: 6vh;" bordered>
        <NText style="font-size: x-large;">
          WACE-VAULT
        </NText>
      </NLayoutHeader>
      <NLayout has-sider>

        <div v-for="[index, popout] in state.popOuts.entries()">
          <MenuPopout v-if="popout.type == 'folder'" :options="popout.data" :index="index" @selected="onmenuSelected"/>
          <FilePopout v-if="popout.type == 'document'" :data="popout.data" :index="index" />
        </div>

        <NLayout>

          <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
            &lt;-- Select an entry on the left
          </div>

        </NLayout>

      </NLayout>
    </NSpace>
  </NConfigProvider>
</template>

<style scoped></style>
