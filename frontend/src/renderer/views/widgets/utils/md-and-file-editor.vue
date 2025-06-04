<template>
  <div class="content">
    <!-- Markdown 编辑 -->
    <div class="markdown-container">
      <md-editor v-model="content"/>
    </div>

    <!-- 附加文件列表 -->
    <download-upload-file-list
        title="已上传文件"
        :editable="true"
        @upload="handleUploadFile"
        @remove="handleRemoveFile"
        :fileList="props.fileList"
        ref="fileUploader"
    />
  </div>
</template>

<script setup lang="ts">
import 'md-editor-v3/lib/style.css';
import {MdEditor} from "md-editor-v3";
import DownloadUploadFileList from "./download-upload-file-list.vue";
import {PropType, ref} from "vue";
import {FileMeta} from "@/types/fileMeta";

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

const content = ref<string>(props.content);
const fileUploader = ref<InstanceType<typeof DownloadUploadFileList>>();

const emit = defineEmits<{
  (e: "upload", file: FileMeta): void;
  (e: "remove", file: FileMeta): void;
}>();

const handleUploadFile = (file: FileMeta) => {
  emit("upload", file)
}

const handleRemoveFile = (file: FileMeta) => {
  emit("remove", file)
}

defineExpose({
  getContent: (): string => content.value,
  updateContent: (data: string): void => {content.value = data},
});
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