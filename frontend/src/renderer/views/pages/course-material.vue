<template>
  <el-scrollbar class="pdf-scroll-container">
    <div class="pdf-container">
      <div v-for="(page, index) in pages" :key="index" class="pdf-page">
        <canvas :ref="(el) => setCanvasRef(el, index)"></canvas>
      </div>
      <div ref="bottomObserver" class="observer"></div>
    </div>
  </el-scrollbar>
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
let totalPages = 0;
const PAGE_BATCH_SIZE = 5;

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

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
  height: 85vh;
  overflow: auto;
}

.pdf-container {
  padding: 0px;
}

.pdf-page {
  display: flex;
  justify-content: center;
  padding: 10px 0;
}
</style>
