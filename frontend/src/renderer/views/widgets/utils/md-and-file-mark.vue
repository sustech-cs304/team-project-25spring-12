<template>
  <div class="content">
    <!-- Markdown 预览 -->
    <div class="container" v-if="!selectedFile">
      <md-preview v-bind="getEditorProps(props.mdContent)"/>
    </div>
    <div class="container" v-else>
      <pdf-viewer ref="pdfViewer" :data="content" is-marking v-if="selectedFileType === FileType.PDF"/>
      <pre style="white-space: pre-wrap" v-else-if="selectedFileType === FileType.PLAIN">{{ content || '加载失败' }}</pre>
      <md-preview v-bind="getEditorProps(content || '加载失败')" v-else-if="selectedFileType === FileType.MARKDOWN"/>
      <ImageZoom :src="content" :alt="selectedFile.filename" v-else-if="selectedFileType === FileType.IMAGE"/>
      <audio controls style="width: 100%" v-else-if="selectedFileType === FileType.AUDIO">
        <source :src="content"/>
        当前浏览器不支持音频播放
      </audio>
      <video controls style="width: 100%" v-else-if="selectedFileType === FileType.VIDEO">
        <source :src="content"/>
        当前浏览器不支持视频播放
      </video>
      <span v-else>暂不支持当前类型文件预览</span>
    </div>

    <!-- 下载文件列表 -->
    <view-file-list
        :file-list="props.fileList"
        :selected-file-id="selectedFileId"
        @update:selected-file-id="handleUpdateSelectFileId"
        v-if="props.fileList"
    />
  </div>
</template>

<script setup lang="ts">
import {computed, ref, watch} from "vue";
import "md-editor-v3/lib/preview.css";
import {MdPreview} from "md-editor-v3";
import ViewFileList from "./view-file-list.vue";
import PdfViewer from "./pdf-viewer.vue";
import ImageZoom from "@/views/widgets/utils/image-zoom.vue";
import {FileMeta} from "@/types/fileMeta";

const props = defineProps<{
  submissionId: number;
  mdContent: string;
  fileList?: FileMeta[];
  downloadFile: (submissionId: number, fileId: string) => Promise<Blob>;
}>();

const emit = defineEmits<{
  (e: "update-file", submissionId: number, fileId: string, dataPromise: Promise<Uint8Array>): void;
}>();

enum FileType {
  PDF,
  PLAIN,
  MARKDOWN,
  IMAGE,
  VIDEO,
  AUDIO,
  UNKNOWN,
}

const getEditorProps = (content: string) => {
  return {
    modelValue: content,
    readOnly: true,
    toolbars: [],
    footers: [],
  };
};

const selectedFileId = ref<string | null>(null);
const selectedFile = computed(() => props.fileList?.find((f) => f.id === selectedFileId.value));
const selectedFileType = computed(() => selectedFile.value ? fileType(selectedFile.value.filename) : FileType.UNKNOWN);
const content = ref();
const pdfViewer = ref();

const isDirty = () => {
  return (FileType.PDF === selectedFileType.value && pdfViewer.value.isDirty()) || [FileType.IMAGE, FileType.VIDEO, FileType.AUDIO].includes(selectedFileType.value);
};

const handleSave = (submissionId: number) => {
  if (selectedFileId.value) {
    if (FileType.PDF === selectedFileType.value) {
      const dataPromise = pdfViewer.value.getDocument();
      if (dataPromise) {
        emit("update-file", submissionId, selectedFileId.value, dataPromise);
      }
    } else if ([FileType.IMAGE, FileType.VIDEO, FileType.AUDIO].includes(selectedFileType.value)) {
      if (content.value) {
        URL.revokeObjectURL(content.value);
      }
    }
  }
};

const updateSelectFileId = async (submissionId: number, fileId: string | null) => {
  if (isDirty()) {
    handleSave(submissionId);
  }
  content.value = null;
  selectedFileId.value = fileId;
  if (fileId) {
    const blob = await props.downloadFile(submissionId, fileId);
    if (FileType.PDF === selectedFileType.value) {
      content.value = blob;
    } else if ([FileType.PLAIN, FileType.MARKDOWN].includes(selectedFileType.value)) {
      content.value = await blob.text();
    } else if ([FileType.IMAGE, FileType.VIDEO, FileType.AUDIO].includes(selectedFileType.value)) {
      content.value = URL.createObjectURL(blob);
    }
  }
};

const handleUpdateSelectFileId = (id: string | null) => {
  updateSelectFileId(props.submissionId, id);
};

const fileType = (filename: string) => {
  const ext = filename.split(".").pop()?.toLowerCase() || "";
  if ("pdf" === ext) return FileType.PDF;
  if ("txt" === ext) return FileType.PLAIN;
  if ("md" === ext) return FileType.MARKDOWN;
  if (["png", "jpg", "jpeg", "gif", "svg"].includes(ext)) return FileType.IMAGE;
  if (["mp4", "avi", "mkv", "mov"].includes(ext)) return FileType.VIDEO;
  if (["mp3", "wav", "flac", "aac"].includes(ext)) return FileType.AUDIO;
  return FileType.UNKNOWN;
};

watch(() => props.submissionId, (newSubmissionId, oldSubmissionId) => {
  updateSelectFileId(oldSubmissionId, null);
});

defineExpose({
  isDirty,
  save: () => handleSave(props.submissionId),
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