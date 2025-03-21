<template>
  <div class="content">
    <!-- Markdown 编辑 -->
    <div class="markdown-container">
      <md-editor v-model="content"/>
    </div>

    <!-- 附加文件列表 -->
    <download-upload-file-list title="已上传文件" :upload="true" :fileList="fileList" ref="fileUploader"/>
  </div>
</template>

<script setup lang="ts">
import 'md-editor-v3/lib/style.css';
import {MdEditor} from "md-editor-v3";
import DownloadUploadFileList from "./download-upload-file-list.vue";
import {ref} from "vue";

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
  fileList: {
    type: Object,
    required: true,
  },
});

const content = ref<String>(JSON.parse(JSON.stringify(props.content)));
const fileList = JSON.parse(JSON.stringify(props.fileList));

const fileUploader = ref<InstanceType<typeof DownloadUploadFileList> | null>(null);

defineExpose({
  getContent: () => content.value,
  getFileList: () => fileUploader?.value?.getFileList() || [],
})
</script>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
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