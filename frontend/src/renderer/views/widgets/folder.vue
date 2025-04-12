<template>
  <widget-card
      :title="folder.name"
      icon="FolderOpened"
      color="teal"
  >
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
  </widget-card>
</template>

<script setup lang="ts">
import type { Folder, FolderPageItem } from '@/types/folder'
import WidgetCard from '@/views/widgets/utils/widget-card.vue'
import { Document } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const props = defineProps<{
  folder: Folder
}>()

const router = useRouter()

const handlePageClick = (page: FolderPageItem) => {
  // TODO: 替换为实际的路由跳转逻辑
  // e.g. router.push(`/page/${page.id}`)
  console.log('Clicked page:', page)
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
