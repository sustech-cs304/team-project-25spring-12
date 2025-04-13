<template>
  <widget-card :title="folder.name" type="folder" style="height: 100%" :callback="callback">
    <el-scrollbar>
      <div class="page-list">
        <div
            class="page-item"
            v-for="page in folder.pages"
            :key="page.id"
            @click="handlePageClick(page)"
        >
          <el-icon class="link-icon"><Document /></el-icon>
          <span class="page-name">{{ page.name }}</span>
        </div>
      </div>
    </el-scrollbar>
    <template #button>
      <el-icon><Plus/></el-icon>
      <span>新增页面</span>
    </template>
  </widget-card>

  <!-- 创建页面对话框 -->
  <el-dialog v-model="dialogVisible" title="页面创建" width="500">
    <p><el-input v-model="newPageTitle" placeholder="请输入标题"></el-input></p>
    <div style="text-align:center; margin-top: 5px;">
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleCreatePage" :disabled="newPageTitle === ''">确认</el-button>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import type { Folder, FolderPageItem } from '@/types/folder'
import WidgetCard from '@/views/widgets/utils/widget-card.vue'
import { Document } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {Page} from "@/types/page";

const props = defineProps<{
  folder: Folder
  canEdit: boolean
}>()

const router = useRouter()

const dialogVisible = ref(false)
const newPageTitle = ref('')
const callback = computed(() => props.canEdit ? showCreatePageDialog : null)

const handlePageClick = (page: FolderPageItem) => {
  // TODO: 替换为实际的路由跳转逻辑
  // e.g. router.push(`/page/${page.id}`)
  console.log('Clicked page:', page)
}

const showCreatePageDialog = () => {
  dialogVisible.value = true
  newPageTitle.value = ''
}

const createPage = async () => {
  try {
    const payload = {
      // TODO
    }
    const response = await axios.post("https://example.com/api/class/page", payload) // TODO: 替换为正确的 api 请求
    // pages.push(response.data)
  } catch(error) {
    console.error(error)
  }
}

const handleCreatePage = () => {
  dialogVisible.value = false
  createPage()
}
</script>

<style scoped>
.page-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 4px 0;
}

.page-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.page-item:hover {
  background-color: #f5f7fa;
}

.link-icon {
  color: #409eff;
  font-size: 18px;
}

.page-name {
  font-weight: 500;
  color: #333;
}
</style>
