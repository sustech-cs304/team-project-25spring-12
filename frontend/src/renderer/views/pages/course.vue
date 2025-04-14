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
          :visible="dialogVisible"
          placement="top"
          :width="180"
          v-if="canEdit"
      >
        <p>
          <el-input v-model="newFolderTitle" placeholder="请输入标题"></el-input>
        </p>
        <div style="text-align:center; margin-top: 5px;">
          <el-button size="small" @click="dialogVisible = false">取消</el-button>
          <el-button size="small" type="primary" @click="handleCreateFolder" :disabled="newFolderTitle === ''">确认</el-button>
        </div>
        <template #reference>
          <el-button @click="showCreateFolderDialog">
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
        <folder-widget
            :folder="activeFolder"
            v-if="activeFolder"
            :can-edit="canEdit"
            :course-id="courseId"
            @create-page="handleCreatePage"
        />
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ComputedRef, nextTick, onMounted, ref, watch} from 'vue'
import {useRoute} from 'vue-router'
import FolderWidget from '@/views/widgets/folder.vue'
import type {Folder, FolderPageItem} from '@/types/folder'
import {createFolder, getFolders} from "@/api/course";
import {useUserStore} from "@/store/user";
import type {Page} from "@/types/page";

const route = useRoute()
const userStore = useUserStore()

const folders = ref<Folder[]>([])
const role = ref<string>(null)
const courseId = ref<number>(0)
const canEdit = computed(() => role.value == 'ta' || role.value == 'teacher')

onMounted(async () => {
  courseId.value = Number(route.params.courseId)

  const response = await getFolders(courseId.value)
  folders.value = response.data as Folder[]

  initActiveFolder()
  role.value = await userStore.getRoleByCourseId(courseId.value)
})

const hoveredFolderId = ref<string>('')

const getMenuItemStyle = (folder: Folder) => {
  const isActive = folder.id.toString() == activeFolderId.value
  const isHovered = folder.id.toString() == hoveredFolderId.value

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
const activeFolder: ComputedRef<Folder | null> = computed(() => folders.value.find(f => f.id == activeFolderId.value))

const toggleCollapse = async () => {
  collapsed.value = !collapsed.value
  await nextTick()
}

const initActiveFolder = () => {
  const id = route.query.folder as string
  const matched = folders.value.find((f) => f.id.toString() === id)
  if (matched) {
    activeFolderId.value = matched.id.toString()
  } else if (foldersSorted.value.length > 0) {
    activeFolderId.value = foldersSorted.value[0].id.toString()
  }
  console.log(activeFolderId.value)
}

const handleMenuSelect = (folderId: string) => {
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

const dialogVisible = ref<boolean>(false)
const newFolderTitle = ref<string>('')

const showCreateFolderDialog = () => {
  dialogVisible.value = true
  newFolderTitle.value = ''
}

const handleCreateFolder = async () => {
  dialogVisible.value = false
  const response = await createFolder({
    name: newFolderTitle.value,
    index: folders.value.length,
  } as Folder, courseId.value)
  folders.value.push(response.data as Folder)
}

const handleCreatePage = (page: Page) => {
  activeFolder.value.pages?.push({id: page.id, name: page.name} as FolderPageItem)
}

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
