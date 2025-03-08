<template>
<!--  <el-text>这里之后写标题、发布日期等，已测试不会影响笔记定位</el-text>-->
<!--  <el-text>123</el-text>-->
<!--  <el-text>123</el-text>-->

  <el-scrollbar class="pdf-scroll-container">
    <div class="pdf-container" ref="pdfContainer">
      <div
          v-for="(page, index) in pages"
          :key="index"
          class="pdf-page"
          @contextmenu.prevent="openContextMenu($event, page)"
      >
        <canvas :ref="(el) => setCanvasRef(el, index)"></canvas>

        <!-- 笔记按钮 -->
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
      <div ref="bottomObserver" class="observer"></div>
    </div>
  </el-scrollbar>

  <!-- 右键菜单 -->
  <el-popover
      v-model:visible="contextMenu.visible"
      trigger="manual"
      placement="bottom-start"
  >
    <template #reference>
      <div v-if="contextMenu.visible" class="context-menu-placeholder" ref="contextMenuRef"></div>
    </template>

    <div class="context-menu-content">
      <el-input v-model="newNoteText" placeholder="输入笔记内容..." />
      <el-button type="primary" size="small" @click="addNote">添加笔记</el-button>
    </div>
  </el-popover>
</template>

<script setup>
import { onMounted, ref, nextTick, toRaw } from "vue";
import * as pdfjsLib from "pdfjs-dist";
import pdfWorker from "pdfjs-dist/build/pdf.worker?url";

const pdfUrl = "/assets/sample-long.pdf";
const pages = ref([]);
const canvasRefs = ref([]);
const pdfInstance = ref(null);
const bottomObserver = ref(null);
const pdfContainer = ref(null);
const contextMenuRef = ref(null);
let totalPages = 0;
const PAGE_BATCH_SIZE = 5;

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const notes = ref([
  { page: 1, x: 390, y: 540, text: "王琦老师" },
  { page: 1, x: 430, y: 200, text: "密码学" },
]);

const activeNote = ref(null);

const contextMenu = ref({ visible: false, x: 0, y: 0, page: 1 });
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
  const endPage = Math.min(startPage + PAGE_BATCH_SIZE - 1, totalPages);

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
    const loadingTask = pdfjsLib.getDocument(pdfUrl);
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

  // 设置菜单位置
  contextMenu.value = {
    visible: true,
    x: relativeX,
    y: relativeY,
    page
  };

  nextTick(() => {
    if (contextMenuRef.value) {
      contextMenuRef.value.style.position = "absolute";
      contextMenuRef.value.style.left = `${relativeX + 15}px`;     // left padding = 15
      contextMenuRef.value.style.top = `${event.clientY - 70}px`;  // height of header = 70
      // 这里的绝对坐标计算不会影响保存的数据，只是微调视觉效果。
      // 事实上 targetRect.left 只有两种取值，分别对应根据左侧快捷栏[是/否]展开，因此这两行的计算其实是类似的。
    }
  });
};

const addNote = () => {
  if (!newNoteText.value.trim()) return;

  notes.value.push({
    page: contextMenu.value.page,
    x: contextMenu.value.x,
    y: contextMenu.value.y,
    text: newNoteText.value
  });
  console.log({
    page: contextMenu.value.page,
    x: contextMenu.value.x,
    y: contextMenu.value.y,
    text: newNoteText.value
  })

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
</script>

<style scoped>
.pdf-scroll-container {
  height: calc(100vh - 145px);
  overflow: auto;
}

.pdf-container {
  position: relative;
}

.pdf-page {
  position: relative;
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
</style>
