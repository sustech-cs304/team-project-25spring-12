<template>
  <div class="content">
    <!-- Markdown 编辑 -->
    <div class="markdown-container">
      <md-editor v-model="text"/>
    </div>

    <!-- 附加文件列表 -->
    <download-upload-file-list title="已上传文件" :upload="true" :file_list="file_list"/>

    <el-button
        type="primary"
        :icon="Upload"
        @click="submit"
        style="width: 120px; margin-left: auto"
    >
      提交作业
    </el-button>
  </div>
</template>

<script setup lang="ts">
import 'md-editor-v3/lib/style.css';
import {MdEditor} from "md-editor-v3";
import DownloadUploadFileList from "./download-upload-file-list.vue";
import {Upload} from "@element-plus/icons-vue";

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  file_list: {
    type: Object,
    required: true,
  },
});

const text = JSON.parse(JSON.stringify(props.text));
const file_list = JSON.parse(JSON.stringify(props.file_list));

const submit = {

}

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
</style>