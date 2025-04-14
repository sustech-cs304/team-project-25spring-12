<template>
  <div class="attachments">
    <el-row justify="space-between">
      <el-text size="large" class="attachment-title">{{ title }}</el-text>
    </el-row>
    <el-divider></el-divider>
    <el-row
        v-for="file in fileList"
        :key="file.url"
        class="attachment-item"
        justify="space-between"
        :class="{selected: file === selectedFile}"
        @click="selectFile(file)"
    >
      <el-col :span="2">
        <el-icon :size="20">
          <component :is="getFileIcon(file.filename)"/>
        </el-icon>
      </el-col>
      <el-col :span="16">
        <el-text truncated>{{ file.filename }}</el-text>
      </el-col>
      <el-col :span="6" class="download-btn">
        <el-button
            type="primary"
            link
            :icon="Download"
            @click.stop="handleDownloadFile(file.url, file.filename)"
        >
          下载
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {Box, Document, Folder, Headset, Picture, Tools, VideoCamera, Download} from "@element-plus/icons-vue";
import {ref} from "vue";
import {downloadFile} from "@/utils/useDownloader";

const props = defineProps({
  fileList: {
    type: Object,
    required: false,
    default: [],
  },
  upload: {
    type: Boolean,
    required: false,
    default: false,
  },
  title: {
    type: String,
    required: true,
  },
});

const fileList = ref(JSON.parse(JSON.stringify(props.fileList)));

const selectedFile = ref<null | Object>(null);

// 向父组件返回选定文件
const emit = defineEmits(["update:selectedFileUrl"]);

// 根据文件后缀返回对应的 Element Plus 图标
const getFileIcon = (filename: string) => {
  const ext = filename.split(".").pop()?.toLowerCase();
  if (["zip", "apk", "rar", "7z", "tar", "gz", "bz2", "xz"].includes(ext || "")) return Box;
  if (["exe", "bat", "sh", "jar", "msi", "app", "com", "vbs"].includes(ext || "")) return Tools;
  if (["png", "jpg", "jpeg", "gif", "svg"].includes(ext || "")) return Picture;
  if (["mp4", "avi", "mkv", "mov"].includes(ext || "")) return VideoCamera;
  if (["pdf", "doc", "docx", "txt", "md"].includes(ext || "")) return Document;
  if (["mp3", "wav", "flac", "aac"].includes(ext || "")) return Headset;
  return Folder;
};

// 下载文件
const handleDownloadFile = async (url: string, filename: string) => {
   try {
     await downloadFile(url, filename);
   } catch (error) {
     console.error('下载失败：', error);
   }
 };

const selectFile = (file: Object) => {
  if (selectedFile.value === file) {
    selectedFile.value = null;
  } else {
    selectedFile.value = file;
  }
  emit("update:selectedFileUrl", selectedFile.value === null ? "" : selectedFile.value.url);
};

// 返回文件列表
defineExpose({
  getFileList: () => JSON.parse(JSON.stringify(fileList.value)),
});
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