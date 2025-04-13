<template>
  <div class="widget-layout">
    <!-- 左侧菜单 -->
    <div class="widget-menu-wrapper" :class="{ collapsed }">
      <!-- 折叠按钮 -->
      <div class="menu-toggle" @click="toggleCollapse">
        <el-icon>
          <component :is="collapsed ? 'ArrowRightBold' : 'ArrowLeftBold'"/>
        </el-icon>
        <span v-if="showTitle" class="menu-title">课程内容</span>
      </div>

      <!-- 文件夹菜单 -->
      <el-menu
          class="widget-menu"
          :default-active="activeFolderId"
          :collapse="collapsed"
          :collapse-transition="true"
          mode="vertical"
          @select="handleMenuSelect"
      >
        <el-menu-item
            v-for="folder in foldersSorted"
            :key="folder.id"
            :index="folder.id.toString()"
            class="hoverable-item"
            :style="getMenuItemStyle(folder)"
            @mouseenter="hoveredFolderId = folder.id"
            @mouseleave="hoveredFolderId = null"
        >
          <el-icon><Folder/></el-icon>
          <span v-if="!collapsed">{{ folder.name }}</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主体内容区域 -->
    <div class="widget-content">
      <el-scrollbar class="widget-scroll-wrapper">
        <folder-widget :folder="activeFolder" v-if="activeFolder"/>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, nextTick, onMounted, ref, watch} from 'vue'
import {useRoute} from 'vue-router'
import FolderWidget from '@/views/widgets/folder.vue'
import type {Folder} from '@/types/folder'
import {getFolders} from "@/api/course";

const route = useRoute()
const folders = ref<Folder[]>([])

onMounted(async () => {
  const response = await getFolders(route.params.courseId)
  folders.value = response.data as Folder[]
  initActiveFolder()
})

const hoveredFolderId = ref<number>(-1)

const getMenuItemStyle = (folder: Folder) => {
  const isActive = folder.id.toString() == activeFolderId.value
  const isHovered = folder.id == hoveredFolderId.value

  const baseColor = '#f9f9f9'
  const hoverColor = '#e6f0ff'
  const activeColor = '#409EFF'

  return {
    backgroundColor: isActive ? activeColor : (isHovered ? hoverColor : baseColor),
    color: isActive ? 'white' : 'black',
    fontWeight: 'bold',
    borderRadius: '6px',
    margin: '4px 8px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    justifyContent: collapsed.value ? 'center' : 'flex-start',
    transition: 'all 0.2s',
    cursor: 'pointer',
  }
}

const collapsed = ref(false)
const showTitle = ref(true)
const foldersSorted = computed(() =>
    [...folders.value].sort((a, b) => a.index - b.index)
)
const activeFolderId = ref('')
const activeFolder = computed(() =>
    folders.value.find((f) => f.id.toString() === activeFolderId.value)
)

const toggleCollapse = async () => {
  collapsed.value = !collapsed.value
  await nextTick()
}

const initActiveFolder = () => {
  const id = route.query.folder as string
  const matched = folders.value.find((f) => f.id.toString() == id)
  if (matched) {
    activeFolderId.value = matched.id.toString()
  } else if (foldersSorted.value.length > 0) {
    activeFolderId.value = foldersSorted.value[0].id.toString()
  }
}

const handleMenuSelect = (folderId: number) => {
  activeFolderId.value = folderId
}

watch(collapsed, (val) => {
  if (val) {
    showTitle.value = false
  } else {
    setTimeout(() => {
      showTitle.value = true
    }, 300)
  }
})
</script>

<style scoped>
.widget-layout {
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.widget-menu {
  height: 100%;
}

.widget-menu-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid #ebeef5;
  transition: width 0.3s ease-in-out;
  width: 300px;
  flex-shrink: 0;
}

.widget-menu-wrapper.collapsed {
  width: 64px;
}

:deep(.el-menu--collapse) {
  width: 64px;
}

.menu-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid #ebeef5;
  transition: padding 0.3s ease-in-out;
}

.menu-title {
  font-weight: bold;
  font-size: 16px;
  transition: opacity 0.3s ease;
  white-space: nowrap;
}

.hoverable-item:hover {
  filter: brightness(1.08);
  cursor: pointer;
}

.widget-content {
  flex: 1;
  height: 100%;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden;
}

.widget-scroll-wrapper {
  height: 100%;
  overflow: auto;
}
</style>
