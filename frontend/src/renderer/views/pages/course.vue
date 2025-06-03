<template>
  <div class="widget-layout">
    <!-- 左侧菜单 -->
    <div class="widget-menu-wrapper">
      <!-- 标题 -->
      <div class="menu-toggle">
        <el-button
            class="back-button"
            @click="goBackToHomepage"
        >
          <el-icon>
            <ArrowLeft/>
          </el-icon>
          <span>返回</span>
        </el-button>
        <span class="menu-title">{{ title }}</span>
      </div>

      <!-- 文件夹菜单 -->
      <el-menu
          class="widget-menu"
          :default-active="activeFolderId"
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
            @mouseleave="hoveredFolderId = ''"
        >
          <el-icon><Folder/></el-icon>
          <span>{{ folder.name }}</span>
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
import {computed, ComputedRef, onMounted, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import FolderWidget from '@/views/widgets/folder.vue'
import type {Folder, FolderPageItem} from '@/types/folder'
import {createFolder, getCourseInfo, getFolders} from "@/api/course";
import {getRoleByCourseId} from "@/composables/useUserData"
import type {Page} from "@/types/page";
import {ArrowLeft} from "@element-plus/icons-vue";
import {Course} from "@/types/course";

const route = useRoute()
const router = useRouter()

const goBackToHomepage = () => {
  router.push('/homepage')
}

const folders = ref<Folder[]>([])
const title = ref<string>('')
const role = ref<string>('')
const courseId = ref<number>(0)
const canEdit = computed(() => role.value == 'teaching assistant' || role.value == 'teacher')

const numberOrNull = (num: number | null) => num ?? 0;

onMounted(async () => {
  courseId.value = Number(route.params.courseId)

  const response = await getFolders(courseId.value)
  folders.value = response.data as Folder[]

  const response2 = await getCourseInfo(courseId.value)
  title.value = (response2.data as Course).name

  // 有一个 id 为 null 的文件夹，收录未分类的页面
  folders.value = (response.data as Folder[]).map(folder => ({
    ...folder,
    id: numberOrNull(folder.id)
  }))

  const uncategorized = folders.value.find(f => f.id === 0);
  if (uncategorized) {
    uncategorized.name = "未分类";
    uncategorized.index = 0;
  }

  initActiveFolder()
  role.value = await getRoleByCourseId(courseId.value)
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
    justifyContent: 'flex-start',
    transition: 'all 0.2s',
    cursor: 'pointer',
  }
}

const foldersSorted = computed(() =>
    [...folders.value].sort((a, b) => a.index - b.index)
)
const activeFolderId = ref('')
const activeFolder: ComputedRef<Folder | null> = computed(() => folders.value.find(f => f.id == activeFolderId.value))

const initActiveFolder = () => {
  const id = route.query.folder as string
  const matched = folders.value.find((f) => f.id.toString() === id)
  if (matched) {
    activeFolderId.value = matched.id.toString()
  } else if (foldersSorted.value.length > 0) {
    activeFolderId.value = foldersSorted.value[0].id.toString()
  }
}

const handleMenuSelect = (folderId: string) => {
  activeFolderId.value = folderId
}

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
  const newFolder = response.data as Folder
  folders.value.push(newFolder)
}

const handleCreatePage = (page: Page) => {
  activeFolder.value.pages?.push({id: page.id, name: page.name} as FolderPageItem)
}

</script>

<style scoped>
.back-button {
  width: 90px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 16px;
  margin: 0;
  height: 100%;
  color: var(--el-color-primary);
}

.back-button span {
  margin-left: 8px;
}

.menu-toggle {
  height: 56px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
}

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

.menu-title {
  font-weight: bold;
  font-size: 16px;
  transition: opacity 0.3s ease;
  white-space: nowrap;
  margin-left: 15px;
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
