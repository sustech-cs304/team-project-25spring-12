<template>
  <div class="content">
    <!-- Markdown 预览 -->
    <div class="markdown-container">
      <md-preview v-bind="editorProps"/>
    </div>

    <!-- 下载文件列表 -->
    <div class="attachments">
      <el-text size="large" class="attachment-title">附件下载</el-text>
      <el-divider></el-divider>
      <el-row
          v-for="file in props.data.attachments"
          :key="file.URL"
          class="attachment-item"
          align="middle"
          justify="space-between"
      >
        <el-col :span="2">
          <el-icon :size="20">
            <component :is="getFileIcon(file.file_name)"/>
          </el-icon>
        </el-col>
        <el-col :span="16">
          <el-text truncated>{{ file.file_name }}</el-text>
        </el-col>
        <el-col :span="6" class="download-btn">
          <el-button
              type="primary"
              link
              :icon="Download"
              @click="downloadFile(file.URL, file.file_name)"
          >
            下载
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import "md-editor-v3/lib/preview.css";
import {MdPreview} from "md-editor-v3";
import {Box, Document, Download, Folder, Headset, Picture, Tools, VideoCamera} from "@element-plus/icons-vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const editorProps = {
  modelValue: props.data.content,
  readOnly: true,
  toolbars: [],
  footers: [],
};

// 根据文件后缀返回对应的 Element Plus 图标
const getFileIcon = (fileName: string) => {
  const ext = fileName.split(".").pop()?.toLowerCase();
  if (["zip", "apk", "rar", "7z", "tar", "gz", "bz2", "xz"].includes(ext || "")) return Box;
  if (["exe", "bat", "sh", "jar", "msi", "app", "com", "vbs"].includes(ext || "")) return Tools;
  if (["png", "jpg", "jpeg", "gif", "svg"].includes(ext || "")) return Picture;
  if (["mp4", "avi", "mkv", "mov"].includes(ext || "")) return VideoCamera;
  if (["pdf", "doc", "docx", "txt", "md"].includes(ext || "")) return Document;
  if (["mp3", "wav", "flac", "aac"].includes(ext || "")) return Headset;
  return Folder;
};

// 下载文件
const downloadFile = (url: string, fileName: string) => {
  // TODO
};
</script>

<style scoped>
.content {
  display: flex;
  gap: 20px;
  padding: 0;
  border-radius: 10px;
}

.markdown-container {
  flex: 1;
  padding: 15px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.attachments {
  width: 350px;
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

.download-btn {
  text-align: right;
}

.el-button {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
}

.el-button:hover {
  background-color: #66b1ff;
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