<template>
  <div class="content">
    <!-- Markdown 预览 -->
    <div class="container" v-if="selectedFileUrl === ''">
      <md-preview v-bind="editorProps"/>
    </div>
    <template
        v-for="file in props.data.attachments"
        :key="file.url"
    >
      <div class="container" v-if="selectedFileUrl === file.url">
        <pdf-viewer :pdf-file="file" :is-marking="true" v-if="file.fileName.endsWith('pdf')"/>
        <span v-else>暂不支持当前类型文件预览</span>
      </div>
    </template>

    <!-- 下载文件列表 -->
    <view-file-list
        :fileList="props.data.attachments"
        @update:selected-file-url="(data) => { selectedFileUrl = data; }"
        title="附件"/>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue";
import "md-editor-v3/lib/preview.css";
import {MdPreview} from "md-editor-v3";
import ViewFileList from "./view-file-list.vue";
import PdfViewer from "./pdf-viewer.vue";

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

const selectedFileUrl = ref("");
</script>

<style scoped>
.content {
  display: flex;
  gap: 20px;
  padding: 0;
  border-radius: 10px;
}

.container {
  flex: 1;
  padding: 15px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>