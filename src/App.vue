<script lang="ts" setup>
import { reactive } from '@vue/reactivity';
import { NConfigProvider, NMenu, NIcon, NSpace, NLayout, NLayoutSider, NScrollbar, NLayoutHeader, NH1, NText, NBreadcrumb, NBreadcrumbItem, NResult, NPopover, NButton } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { darkTheme } from 'naive-ui';
import { DocumentOutline, FolderOutline } from "@vicons/ionicons5"
import { h } from 'vue'
import type { VNode, Component } from 'vue'
import MenuPopout from './components/MenuPopout.vue';
import FilePopout from './components/FilePopout.vue';
import type { VaultDocument } from './types/interfaces'
import hljs from 'highlight.js/lib/core'

interface FolderPopoutData {
  name: string
  type: 'folder',
  data: MenuOption[]
  folderData: any
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
  popOuts: PopoutData[],
  errored: boolean
}>({
  popOuts: [],
  errored: false
})

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

// Convert the file index tree into menu options format
const indexDataToMenuOptions = (data: any): FileMenuOption[] => {
  return Object.entries(data).map(entry => {
    //@ts-ignore
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
        //@ts-ignore
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
  try {
    const res = await fetch('/collection/index.json')
    const data = await res.json()
    //@ts-ignore
    state.popOuts.push({
      type: 'folder',
      data: indexDataToMenuOptions(data.resources),
      folderData: data.resources,
      name: 'collection'
    })
  } catch {
    state.errored = true
  }
}

// A menu has its active item changed
const onmenuSelected = (option: string, index: number) => {
  //First close all popouts after this menu(if any)
  state.popOuts.splice(index + 1)

  //@ts-ignore
  const optionData: FileMenuOption | undefined = (state.popOuts[index] as FolderPopoutData).data
    .find(d => d.key == option)

  if (!optionData) return

  if (optionData.type == 'folder') {
    state.popOuts.push({
      type: 'folder',
      data: indexDataToMenuOptions(optionData.data),
      folderData: optionData.data,
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
  <NConfigProvider :theme="darkTheme" :hljs="hljs">
    <NSpace vertical style="gap: none;">

      <NLayoutHeader style="padding: 5px; height: 80px;" bordered>
        <NText style="font-size: x-large;">
          WACE-VAULT
        </NText>
        <a href='https://github.com/skybird23333/collection' target="_blank">
          <n-button strong secondary type="info" style="margin-left: 10px;">
            Github
          </n-button>
        </a>

        <n-popover trigger="hover" :width="30">
          <template #trigger>
            <n-button strong secondary type="warning" style="margin-left: 10px;"><b>
                [?] This is an unofficial mirror
              </b>
            </n-button>
          </template>
          <span>
            <b>WACE Vault has been shut down since Mar 26.</b> The resources of this site is hosted by another
            individual
            with no affiliations with the WACE Vault team, under their own risks and responsibilities. The front end of
            this website is created by said individual. If you have issues navigating the site, open an issue on the
            Github page. If you have any other queries, direct it to 2603003199a@gmail.com.
          </span>
        </n-popover>

        <n-popover trigger="hover" :width="30">
          <template #trigger>
            <n-button strong secondary style="margin-left: 10px;">
              [?] how can I bulk download files?
            </n-button>
          </template>
          <span>
            Depending on the number of files you require, either download them individually or download the entire
            repository
            using the Github page. Click on "Code" then "Download ZIP". The size of the repository is stated on the left
            of the
            page.
          </span>
        </n-popover>


        <NBreadcrumb>
          <NBreadcrumbItem v-for="[index, popout] in state.popOuts.entries()" :key="index" :clickable="false">
            <NIcon>
              <FolderOutline v-if="popout.type === 'folder'" />
              <DocumentOutline v-if="popout.type === 'document'" />
            </NIcon>
            {{ popout.name }}
          </NBreadcrumbItem>
        </NBreadcrumb>
      </NLayoutHeader>


      <NScrollbar :x-scrollable="true">

        <NLayout has-sider>

          <div v-for="[index, popout] in state.popOuts.entries()" :key="index">
            <MenuPopout v-if="popout.type == 'folder'" :options="popout.data" :index="index" :name="popout.name"
              @selected="onmenuSelected" :collapsed="(state.popOuts.length - index > 2)"
              :folderData="popout.folderData" />
          </div>

          <NLayout v-if="state.popOuts.length > 0" has-sider>
            <FilePopout v-if="state.popOuts[state.popOuts.length - 1].type == 'document'"
              :data="state.popOuts[state.popOuts.length - 1].data" />
          </NLayout>

          <NLayout v-if="state.errored" style="height: 92vh; overflow: hidden;">
            <NResult status="500" title="Failed to fetch the index file"
              description="The vault app depends on an index file to work, which may have not been included in the build for some reason. Please open an issue."
              style="padding: 20%; height: 100%; overflow: hidden;">
            </NResult>
          </NLayout>
        </NLayout>


      </NScrollbar>
    </NSpace>
  </NConfigProvider>
</template>

<style scoped></style>
