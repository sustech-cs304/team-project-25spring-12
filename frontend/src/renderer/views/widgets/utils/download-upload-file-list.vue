<template>
  <div class="attachments">
    <el-row justify="space-between">
      <el-text size="large" class="attachment-title">{{ title }}</el-text>
      <el-upload
          v-show="editable"
          :http-request="handleUpload"
          :show-file-list="false"
      >
        <el-button type="primary">上传文件</el-button>
      </el-upload>
    </el-row>

    <el-divider/>

    <el-row
        v-for="file in fileList"
        :key="file.id"
        class="attachment-item"
        justify="space-between"
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
            v-if="editable"
            type="danger"
            link
            :icon="Delete"
            @click="handleRemoveFile(file.id)"
        >
          删除
        </el-button>

        <el-button
            type="primary"
            link
            :icon="Download"
            @click="handleDownloadFile(file)"
        >
          下载
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {ElMessage} from "element-plus";
import {Download, Delete} from "@element-plus/icons-vue";
import {PropType} from "vue";
import {getFileIcon} from "@/utils/getIconByFileType";
import {FileMeta} from "@/types/fileMeta";
import {useUploader} from "@/composables/useUploader";
import {useDownloader} from "@/composables/useDownloader";

const props = defineProps({
  fileList: {
    type: Array as PropType<FileMeta[]>,
    required: true,
  },
  editable: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    required: true,
  },
});

const emit = defineEmits<{
  (e: "upload", file: FileMeta): void;
  (e: "remove", file: FileMeta): void;
}>();

// 如果进一步解耦，这里可以变成两个 props 由用户决定上传和下载的组合逻辑
// 但是在本项目中上传下载的逻辑是固定的，因此没有进一步解耦
const {upload} = useUploader();
const {download} = useDownloader();

// 下载文件
const handleDownloadFile = async (file: FileMeta) => {  // 本项目中，目前 file.url 为空
  try {
    await download(file);
  } catch (error) {
    ElMessage.error("下载失败，请稍后重试");
  }
};

// 上传文件
const handleUpload = async (options: any) => {
  const {file, onSuccess, onError} = options;

  try {
    const result = await upload(file);
    emit("upload", result as FileMeta);
    onSuccess(result);
  } catch (err) {
    ElMessage.error("上传失败，请稍后重试");
    onError(err);
  }
};

// 删除文件
const handleRemoveFile = async (fileId: string) => {
  // 本项目中删除文件无需告知后端，后端会离线扫描没有引用的文件进行删除
  emit("remove", fileId);
}
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
