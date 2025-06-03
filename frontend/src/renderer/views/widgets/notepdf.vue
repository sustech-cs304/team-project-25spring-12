<template>
  <widget-card :title="computedTitle" type="notepdf" :button-visible="props.editable" @click="handleClick">
    <div class="card-content">
      <el-text>提示：在课件任意位置右键，创建一条笔记！</el-text>
      <el-button type="primary" :icon="Download" @click="handleDownload">下载原课件</el-button>
    </div>

    <el-scrollbar class="pdf-scroll-container">
      <div class="pdf-container" ref="pdfContainer">
        <div
            v-for="(page, index) in pages"
            :key="page"
            class="pdf-page"
            @contextmenu.prevent="openContextMenu($event, page)"
        >
          <canvas :ref="el => setCanvasRef(el, index)"></canvas>

          <el-tooltip
              v-for="note in getNotesForPage(page)"
              :key="note.id"
              effect="dark"
              :content="note.text"
              placement="top"
          >
            <div
                class="note-button"
                :style="{ left: `${note.x}px`, top: `${note.y}px` }"
                @click="toggleNote(note)"
            ></div>
          </el-tooltip>
        </div>

        <div ref="bottomObserver" class="observer"></div>
      </div>
    </el-scrollbar>

    <!-- 添加笔记弹窗 -->
    <el-popover
        v-model:visible="contextMenu.visible"
        placement="bottom-start"
        teleported
        popper-class="custom-popover"
        :popper-style="{
        top: `${popoverPosition.y}px`,
        left: `${popoverPosition.x}px`,
        'max-height': '90px',
        overflow: 'hidden',
      }"
    >
      <template #reference>
        <div v-show="contextMenu.visible" class="context-menu-placeholder" ref="contextMenuRef"/>
      </template>

      <div class="context-menu-content">
        <el-input v-model="newNoteText" placeholder="输入笔记内容..."/>
        <el-button type="primary" size="small" @click="addNote">添加笔记</el-button>
      </div>
    </el-popover>
    <template #button>
      <el-upload
          ref="uploadRef"
          :show-file-list="false"
          :http-request="handleUpload"
      >
        <el-icon>
          <Upload/>
        </el-icon>
        <span>上传</span>
      </el-upload>
    </template>
  </widget-card>
</template>

<script setup lang="ts">
import {computed, nextTick, onMounted, ref, toRaw} from 'vue';
import * as pdfjsLib from 'pdfjs-dist';
import pdfWorker from 'pdfjs-dist/build/pdf.worker?url';
import {Download} from '@element-plus/icons-vue';
import widgetCard from './utils/widget-card.vue';
import type {Note, NotePdfWidget} from '@/types/widgets';
import {Upload} from "@element-plus/icons-vue";
import {createNote, editNotePdfWidget} from "@/api/courseMaterial";
import {useDownloader} from "@/composables/useDownloader";
import {useUploader} from "@/composables/useUploader";
import {ElMessage} from "element-plus";
import {FileMeta} from "@/types/fileMeta";
import {WidgetUnion} from "@/types/widgets";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const {getFile, download} = useDownloader()
const {upload} = useUploader()

const props = defineProps<{
  data: NotePdfWidget;
  editable: boolean;
}>();

const computedTitle = computed(() => props.data.title || "互动式课件");

// refs
const pages = ref<number[]>([]);
const canvasRefs = ref<(HTMLCanvasElement | undefined)[]>([]);
const pdfInstance = ref<pdfjsLib.PDFDocumentProxy | null>(null);
const bottomObserver = ref<HTMLElement | null>(null);
const pdfContainer = ref<HTMLElement | null>(null);

const notes = ref<Note[]>(props.data.notes);
const contextMenuRef = ref<HTMLElement | null>(null);
const activeNote = ref<Note | null>(null);
const contextMenu = ref({
  visible: false,
  x: 0,
  y: 0,
  page: 1,
});
const popoverPosition = ref({x: 0, y: 0});
const newNoteText = ref('');
let totalPages = 0;
const pageBatchSize = 5;

// canvas 操作
const setCanvasRef = (el: HTMLCanvasElement | null, index: number) => {
  if (el) canvasRefs.value[index] = el;
};

const renderPage = async (pageNumber: number) => {
  if (!pdfInstance.value) return;
  const rawPdf = toRaw(pdfInstance.value);
  try {
    const page = await rawPdf.getPage(pageNumber);
    const scale = 1.5;
    const viewport = page.getViewport({scale});
    const canvas = canvasRefs.value[pageNumber - 1];
    if (!canvas) return;

    canvas.width = viewport.width;
    canvas.height = viewport.height;

    const context = canvas.getContext('2d');
    if (!context) return;

    await page.render({canvasContext: context, viewport}).promise;
  } catch (error) {
    console.error(`Error rendering page ${pageNumber}:`, error);
  }
};

const loadMorePages = async () => {
  if (!pdfInstance.value) return;

  const start = pages.value.length + 1;
  const end = Math.min(start + pageBatchSize - 1, totalPages);

  for (let i = start; i <= end; i++) {
    pages.value.push(i);
  }

  await nextTick();

  for (let i = start; i <= end; i++) {
    await renderPage(i);
  }
};

const loadPDF = async () => {
  try {
    const blob = await getFile(props.data.pdfFile);
    const arrayBuffer = await blob.arrayBuffer();
    const loadingTask = pdfjsLib.getDocument({data: arrayBuffer});
    pdfInstance.value = await loadingTask.promise;

    totalPages = pdfInstance.value.numPages;
    await loadMorePages();
  } catch (error) {
    console.error("Error loading PDF:", error);
  }
};

const getNotesForPage = (page: number): Note[] => {
  return notes.value.filter(note => note.page === page);
};

const toggleNote = (note: Note) => {
  activeNote.value = activeNote.value === note ? null : note;
};

// 右键打开菜单
const openContextMenu = (event, page) => {
  event.preventDefault();

  // 计算相对于 PDF 页面的坐标
  const targetRect = event.currentTarget.getBoundingClientRect();
  const relativeX = event.clientX - targetRect.left;
  const relativeY = event.clientY - targetRect.top;

  // 存储笔记的位置信息
  contextMenu.value = {
    visible: true,
    x: relativeX,
    y: relativeY,
    page,
  };

  // 设置弹窗位置
  nextTick(() => {
    popoverPosition.value = {x: event.clientX, y: event.clientY};
  });
};

const addNote = () => {
  const text = newNoteText.value.trim();
  if (!text) return;

  const newNote: Note = {
    page: contextMenu.value.page,
    x: contextMenu.value.x,
    y: contextMenu.value.y,
    text,
  } as Note;

  notes.value.push(newNote);
  createNote(newNote, props.data.id);

  newNoteText.value = "";
  contextMenu.value.visible = false;
};

const observeBottom = () => {
  if (!bottomObserver.value) return;

  const observer = new IntersectionObserver(
      entries => {
        const entry = entries[0];
        if (entry.isIntersecting && pages.value.length < totalPages) {
          loadMorePages();
        }
      },
      {rootMargin: "100px"}
  );

  observer.observe(bottomObserver.value);
};

const emit = defineEmits<{
  (e: "update", data: WidgetUnion): void;
}>();

const handleUpload = async (options: any) => {
  const {file, onSuccess, onError} = options;

  try {
    const response = await upload(file);
    if (response.status === 200) {
      const uuid = (response.data as FileMeta).id;
      const newData = JSON.parse(JSON.stringify(props.data));
      newData.pdfFile = uuid;
      const response2 = await editNotePdfWidget(newData);
      if (response2.status === 200) {
        ElMessage.success("上传成功");
        emit("update", newData);
        onSuccess(newData);
      } else {
        ElMessage.error("上传失败，请稍后再试");
        onError(response2);
      }
    } else {
      ElMessage.error("上传失败，请稍后再试");
      onError(response);
    }
  } catch (err) {
    ElMessage.error("上传失败，未知错误");
    onError(err);
  }
};

const handleDownload = async () => {
  try {
    await download(props.data.pdfFile);
  } catch (error) {
    console.error('下载失败：', error);
  }
};

const handleClick = () => {
  upload()
}

onMounted(() => {
  loadPDF();
  observeBottom();
});

defineExpose({
  init: () => {
  }
});
</script>

<style scoped>
.card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.pdf-scroll-container {
  height: calc(100vh - 145px);
  overflow: auto;
  display: flex;
  justify-content: center;
}

.pdf-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pdf-page {
  position: relative;
  margin: 0 auto;
  width: 100%;
}

.note-button {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: radial-gradient(circle, white 30%, rgba(50, 50, 50, 1) 80%);
  position: absolute;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.note-button:hover {
  transform: scale(1.2);
  box-shadow: 0px 0px 5px rgba(50, 50, 50, 0.5);
}

.context-menu-placeholder {
  width: 1px;
  height: 1px;
}

.context-menu-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.custom-popover {
  padding: 0 !important;
  position: absolute !important;
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
</style>
