<template>
  <widget-card :title="computedTitle" icon="DataAnalysis" color="blue">
    <div class="card-content">
      <el-text>
        提示：在课件任意位置右键，创建一条笔记！
      </el-text>
      <el-button type="primary" :icon="Download" @click="handleDownloadFile">
        下载原课件
      </el-button>
    </div>

    <el-scrollbar class="pdf-scroll-container">
      <div class="pdf-container" ref="pdfContainer">
        <div
            v-for="(page, index) in pages"
            :key="index"
            class="pdf-page"
            @contextmenu.prevent="openContextMenu($event, page)"
        >
          <!--   渲染一页 pdf   -->
          <canvas :ref="(el) => setCanvasRef(el, index)"></canvas>

          <!--   在这一页上渲染笔记   -->
          <el-tooltip
              v-for="(note, noteIndex) in getNotesForPage(page)"
              :key="noteIndex"
              effect="dark"
              :content="note.text"
              placement="top"
          >
            <div
                class="note-button"
                :style="{ left: note.x + 'px', top: note.y + 'px' }"
                @click="toggleNote(note)"
            ></div>
          </el-tooltip>
        </div>

        <!--   监听用户处于底部，加载新的页面   -->
        <div ref="bottomObserver" class="observer"></div>
      </div>
    </el-scrollbar>

    <!--   右键添加笔记   -->
    <el-popover
        v-model:visible="contextMenu.visible"
        trigger="manual"
        placement="bottom-start"
        teleported
        popper-class="custom-popover"
        :popper-style="{ top: `${popoverPosition.y}px`, left: `${popoverPosition.x}px`,
            'max-height': '90px', 'overflow': 'hidden' }"
    >
      <template #reference>
        <div v-show="contextMenu.visible" class="context-menu-placeholder" ref="contextMenuRef"></div>
      </template>

      <div class="context-menu-content">
        <el-input v-model="newNoteText" placeholder="输入笔记内容..." />
        <el-button type="primary" size="small" @click="addNote">添加笔记</el-button>
      </div>
    </el-popover>
  </widget-card>
</template>

<script setup>
import { Download } from '@element-plus/icons-vue';
import { onMounted, ref, nextTick, toRaw, computed } from "vue";
import * as pdfjsLib from "pdfjs-dist";
import pdfWorker from "pdfjs-dist/build/pdf.worker?url";
import widgetCard from "./utils/widget-card.vue";
import {downloadFile} from '@/utils/useDownloader';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const computedTitle = computed(() => {
  return props.data?.title || "互动式课件";
});

// pdf渲染
const pages = ref([]);
const canvasRefs = ref([]);
const pdfInstance = ref(null);
const bottomObserver = ref(null);
const pdfContainer = ref(null);
let totalPages = 0;
const pageBatchSize = 5;

// 笔记
const notes = ref(JSON.parse(JSON.stringify(props.data.notes)));
const contextMenuRef = ref(null);
const activeNote = ref(null);
const contextMenu = ref({ visible: false, x: 0, y: 0, page: 1 });
const popoverPosition = ref({x: 0, y: 0});
const newNoteText = ref("");

const setCanvasRef = (el, index) => {
  if (el) {
    canvasRefs.value[index] = el;
  }
};

const renderPage = async (pageNumber) => {
  if (!pdfInstance.value) return;

  const rawPdfInstance = toRaw(pdfInstance.value);
  try {
    const page = await rawPdfInstance.getPage(pageNumber);
    const scale = 1.5;
    const viewport = page.getViewport({ scale });

    const canvas = canvasRefs.value[pageNumber - 1];
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    const context = canvas.getContext("2d");

    await page.render({ canvasContext: context, viewport }).promise;
  } catch (error) {
    console.error(`Error rendering page ${pageNumber}:`, error);
  }
};

const loadMorePages = async () => {
  if (!pdfInstance.value) return;

  const startPage = pages.value.length + 1;
  const endPage = Math.min(startPage + pageBatchSize - 1, totalPages);

  for (let i = startPage; i <= endPage; i++) {
    pages.value.push(i);
  }

  await nextTick();

  for (let i = startPage; i <= endPage; i++) {
    await renderPage(i);
  }
};

const loadPDF = async () => {
  try {
    // 从给定的 URL 读取一个pdf文件
    // 下载并没有采用流式传输：pdf文件的下载速度远大于加载（渲染）速度
    const loadingTask = pdfjsLib.getDocument(props.data.pdfFile.url);
    pdfInstance.value = await loadingTask.promise;

    totalPages = pdfInstance.value.numPages;
    await loadMorePages();
  } catch (error) {
    console.error("Error loading PDF:", error);
  }
};

const getNotesForPage = (page) => {
  return notes.value.filter((note) => note.page === page);
};

const toggleNote = (note) => {
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
    popoverPosition.value.x = event.clientX;
    popoverPosition.value.y = event.clientY;
  });
};

const addNote = () => {
  if (!newNoteText.value.trim()) return;

  notes.value.push({
    page: contextMenu.value.page,
    x: contextMenu.value.x,
    y: contextMenu.value.y,
    text: newNoteText.value,
  });

  // TODO: 上传到后端

  newNoteText.value = "";
  contextMenu.value.visible = false;
};

const observeBottom = () => {
  if (!bottomObserver.value) return;

  const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (entry.isIntersecting && pages.value.length < totalPages) {
          loadMorePages();
        }
      },
      { rootMargin: "100px" }
  );

  observer.observe(bottomObserver.value);
};

onMounted(async () => {
  await loadPDF();
  observeBottom();
});

// 下载原课件
const handleDownloadFile = async () => {
  try {
    await downloadFile(props.data.pdfFile.url, props.data.pdfFile.fileName);
  } catch (error) {
    console.error('下载失败：', error);
  }
};
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

.el-icon {
  color: #409eff;
}
</style>
