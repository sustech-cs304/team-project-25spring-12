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
      <el-popover
          :visible="showCreateFolderPopover"
          placement="top"
          :width="180"
          v-if="authenticated"
      >
        <p>
          <el-input v-model="newFolderTitle" placeholder="请输入标题"></el-input>
        </p>
        <div style="text-align:center; margin-top: 5px;">
          <el-button size="small" @click="showCreateFolderPopover = false">取消</el-button>
          <el-button size="small" type="primary" @click="handleCreateFolder" :disabled="newFolderTitle === ''">确认</el-button>
        </div>
        <template #reference>
          <el-button @click="handleShowCreateFolderPopover()">
            <el-icon>
              <Plus/>
            </el-icon>
            <span>新建目录</span>
          </el-button>
        </template>
      </el-popover>
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
import axios from 'axios'
import FolderWidget from '@/views/widgets/folder.vue'
import type {Folder as FolderType} from '@/types/folder'

const route = useRoute()

const authenticated = ref<boolean>(true) // TODO: 鉴权

const folders: FolderType[] = [
  {
    id: 1,
    index: 0,
    name: '课程介绍',
    visible: true,
    pages: [
      {id: 101, name: '课程大纲'},
      {id: 102, name: '评分标准'},
    ],
  },
  {
    id: 2,
    index: 1,
    name: '课件资料',
    visible: true,
    pages: [
      {id: 201, name: '第一章：绪论'},
      {id: 202, name: '第二章：基本概念'},
      {id: 203, name: '第三章：高级内容'},
    ],
  },
  {
    id: 3,
    index: 2,
    name: '作业与练习',
    visible: true,
    pages: [
      {id: 301, name: '作业一'},
      {id: 302, name: '作业二'},
    ],
  },
  {
    id: 4,
    index: 3,
    name: '通知公告',
    visible: true,
    pages: [
      {id: 401, name: '开课通知'},
      {id: 402, name: '期中提醒'},
      {id: 403, name: '期末安排'},
    ],
  },
]

const hoveredFolderId = ref<number | null>(null)

const showCreateFolderPopover = ref<boolean>(false);
const newFolderTitle = ref<string>('')

const handleShowCreateFolderPopover = () => {
  newFolderTitle.value = ''
  showCreateFolderPopover.value = true
}

const createFolder = async () => {
  try {
    const payload = {
      classId: 0, // TODO: 修改为正确的 classId
      index: folders.length,
      name: newFolderTitle.value,
    }
    const response = await axios.post("https://example.com/api/class/folder", payload) // TODO: 替换为正确的 api 请求
    folders.push(response.data) // TODO: 确认响应内容符合预期
  } catch(error) {
    console.error(error)
  }
}

const handleCreateFolder = () => {
  showCreateFolderPopover.value = false
  createFolder()
}

const getMenuItemStyle = (folder: FolderType) => {
  const isActive = folder.id.toString() === activeFolderId.value
  const isHovered = folder.id === hoveredFolderId.value

  const baseColor = '#f9f9f9'
  const hoverColor = '#e6f0ff'
  const activeColor = '#409EFF'

  return {
    backgroundColor: isActive
        ? activeColor
        : isHovered
            ? hoverColor
            : baseColor,
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
    [...folders].sort((a, b) => a.index - b.index)
)
const activeFolderId = ref('')
const activeFolder = computed(() =>
    folders.find((f) => f.id.toString() === activeFolderId.value)
)

const toggleCollapse = async () => {
  collapsed.value = !collapsed.value
  await nextTick()
}

const initActiveFolder = () => {
  const id = route.query.folder as string
  const matched = folders.find((f) => f.id.toString() === id)
  if (matched) {
    activeFolderId.value = matched.id.toString()
  } else if (foldersSorted.value.length > 0) {
    activeFolderId.value = foldersSorted.value[0].id.toString()
  }
}

const handleMenuSelect = (folderId: string) => {
  activeFolderId.value = folderId
}

onMounted(() => {
  initActiveFolder()
})

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
