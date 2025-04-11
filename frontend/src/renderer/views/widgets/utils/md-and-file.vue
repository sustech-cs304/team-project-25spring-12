<template>
  <div class="content">
    <!-- Markdown 预览 -->
    <div class="markdown-container">
      <md-preview v-bind="editorProps"/>
    </div>

    <!-- 下载文件列表 -->
    <download-upload-file-list :fileList="props.fileList" title="下载附件"/>
  </div>
</template>

<script setup lang="ts">
import "md-editor-v3/lib/preview.css";
import {MdPreview} from "md-editor-v3";
import DownloadUploadFileList from "./download-upload-file-list.vue";
import {PropType} from "vue";
import {FileMeta} from "@/types/widgets";

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
  fileList: {
    type: Array as PropType<FileMeta[]>,
    required: false,
    default: () => []
  },
});

const editorProps = {
  modelValue: props.content,
  readOnly: true,
  toolbars: [],
  footers: [],
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
</style>