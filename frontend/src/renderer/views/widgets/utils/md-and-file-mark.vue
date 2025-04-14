<template>
  <div class="content">
    <!-- Markdown 预览 -->
    <div class="container" v-if="selectedFileUrl === ''">
      <md-preview v-bind="getEditorProps(props.data.content)"/>
    </div>
    <template
        v-for="file in props.data.attachments"
        :key="file.url"
    >
      <div class="container" v-if="selectedFileUrl === file.url">
        <pdf-viewer :pdf-file="file" :is-marking="true" v-if="fileType(file.filename) === 'pdf'"/>
        <pre style="white-space: pre-wrap" v-else-if="fileType(file.filename) === 'plain'">{{ textContents[file.url] || "加载失败" }}</pre>
        <md-preview v-bind="getEditorProps(textContents[file.url] || '加载失败')" v-else-if="fileType(file.filename) === 'markdown'"/>
        <ImageZoom :src="file.url" :alt="file.filename" v-else-if="fileType(file.filename) === 'image'"/>
        <audio controls style="width: 100%" v-else-if="fileType(file.filename) === 'audio'">
          <source :src="file.url"/>
          当前浏览器不支持音频播放
        </audio>
        <video controls style="width: 100%" v-else-if="fileType(file.filename) === 'video'">
          <source :src="file.url"/>
          当前浏览器不支持视频播放
        </video>
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
import {onMounted, ref} from "vue";
import "md-editor-v3/lib/preview.css";
import {MdPreview} from "md-editor-v3";
import ViewFileList from "./view-file-list.vue";
import PdfViewer from "./pdf-viewer.vue";
import ImageZoom from "@/views/widgets/utils/image-zoom.vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const getEditorProps = (content: string) => {
  return {
    modelValue: content,
    readOnly: true,
    toolbars: [],
    footers: [],
  };
};

const textContents = ref({});

const selectedFileUrl = ref("");

const fileType = (filename: string) => {
  const ext = filename.split(".").pop()?.toLowerCase() || "";
  if ("pdf" === ext) return "pdf";
  if ("txt" === ext) return "plain";
  if ("md" === ext) return "markdown";
  if (["png", "jpg", "jpeg", "gif", "svg"].includes(ext)) return "image";
  if (["mp4", "avi", "mkv", "mov"].includes(ext)) return "video";
  if (["mp3", "wav", "flac", "aac"].includes(ext)) return "audio";
  return "unknown";
};

onMounted(() => {
  for (let file of props.data.attachments) {
    if (["plain", "markdown"].includes(fileType(file.filename))) {
      fetch(file.url).then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to fetch file from ${file.url}: ${response.statusText}`);
        }
        return response.text();
      }).then((text) => {
        textContents.value[file.url] = text;
      }).catch((error) => {
        console.error(error);
      });
    }
  }
});
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