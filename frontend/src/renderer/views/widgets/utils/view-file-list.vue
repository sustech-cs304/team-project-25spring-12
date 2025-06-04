<template>
  <div class="attachments">
    <el-row justify="space-between">
      <el-text size="large" class="attachment-title">附件</el-text>
    </el-row>

    <el-divider/>

    <el-row
        v-for="file in fileList"
        :key="file.id"
        class="attachment-item"
        :class="{'selected': props.selectedFileId === file.id}"
        justify="space-between"
        @click="handleSelectFile(file)"
    >
      <el-col :span="2">
        <el-icon :size="20">
          <component :is="getFileIcon(file.filename)"/>
        </el-icon>
      </el-col>

      <el-col :span="12">
        <el-text truncated>{{ file.filename }}</el-text>
      </el-col>

      <el-col :span="10" class="download-btn">
        <el-button
            type="primary"
            link
            :icon="Download"
            @click.stop="handleDownloadFile(file)"
        >
          下载
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {ElMessage} from "element-plus";
import {Download} from "@element-plus/icons-vue";
import {getFileIcon} from "@/utils/getIconByFileType";
import type {FileMeta} from "@/types/fileMeta";
import {useDownloader} from "@/composables/useDownloader";

const props = defineProps<{
  fileList: FileMeta[];
  selectedFileId: string | null;
}>();

const emit = defineEmits<{
  (e: "update:selectedFileId", id: string | null): void;
}>();

// 如果进一步解耦，这里可以变成两个 props 由用户决定上传和下载的组合逻辑
// 但是在本项目中上传下载的逻辑是固定的，因此没有进一步解耦
const {download} = useDownloader();

// 选择文件
const handleSelectFile = (file: FileMeta) => {
  if (props.selectedFileId === file.id) {
    emit("update:selectedFileId", null);
  } else {
    emit("update:selectedFileId", file.id);
  }
};

// 下载文件
const handleDownloadFile = async (file: FileMeta) => {  // 本项目中，目前 file.url 为空
  try {
    await download(file);
  } catch (error) {
    ElMessage.error("下载失败，请稍后重试");
  }
};
</script>

<style scoped>
.attachments {
  min-width: 350px;
  background: #f9fafb;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.attachment-title {
  font-weight: bold;
  font-size: 18px;
  color: #333;
}

.attachment-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.attachment-item:hover {
  background: #f1f1f1;
}

.selected {
  background: #d9d9d9;
}

.download-btn {
  text-align: right;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.el-button {
  font-size: 14px;
  border-radius: 8px;
}

.el-text {
  font-size: 14px;
  color: #666;
}

.el-divider {
  margin: 10px 0;
}

.el-icon {
  color: #409eff;
}
</style>
