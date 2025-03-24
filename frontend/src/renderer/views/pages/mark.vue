<template>
  <div class="page">
    <div>
      <el-button @click="pointerMode" :type="mode == 0 ? 'primary' : ''">
        指针
      </el-button>
      <el-button @click="inkMode" :type="mode == 1 ? 'primary' : ''">
        绘画
      </el-button>
      <el-button @click="highlightMode" :type="mode == 2 ? 'primary' : ''">
        高亮
      </el-button>
      <el-button @click="freeTextMode" :type="mode == 3 ? 'primary' : ''">
        文字
      </el-button>
      <div class="pdfHost">
        <div class="viewerContainer" ref="viewerContainer">
          <div class="pdfViewer"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import * as pdfjsLib from "pdfjs-dist";
import * as pdfjsViewer from "pdfjs-dist/web/pdf_viewer.mjs";
import pdfWorker from "pdfjs-dist/build/pdf.worker?url";
import "pdfjs-dist/web/pdf_viewer.css";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const props = {
  data: {
    pdfFile: 'https://arxiv.org/pdf/2403.14740',
  },
};

const mode = ref(0);
const viewerContainer = ref();
var pdfViewer: pdfjsViewer.PDFViewer;
var resizeObserver = new ResizeObserver((entries) => {
  if (entries.length > 0) {
    pdfViewer.currentScaleValue = "page-width";
  }
});

const loadPDF = async () => {
  try {
    const container = viewerContainer.value;
    const eventBus = new pdfjsViewer.EventBus();
    pdfViewer = new pdfjsViewer.PDFViewer({
      container,
      eventBus,
      annotationEditorHighlightColors: "yellow=#FFFF98,green=#53FFBC,blue=#80EBFF,pink=#FFCBE6,red=#FF4F5F",
    });
    eventBus.on("pagesinit", function () {
      pdfViewer.currentScaleValue = "page-width";
    })
    const loadingTask = pdfjsLib.getDocument(props.data.pdfFile);
    const pdfDocument = await loadingTask.promise;
    pdfViewer.setDocument(pdfDocument);
    resizeObserver.observe(container);
  } catch (e) {
    console.error(`Error rendering pdf:`, e);
  }
};

const pointerMode = () => {
  mode.value = 0;
  pdfViewer.annotationEditorMode = { mode: pdfjsLib.AnnotationEditorType.NONE };
};

const inkMode = () => {
  mode.value = 1;
  pdfViewer.annotationEditorMode = { mode: pdfjsLib.AnnotationEditorType.INK };
};

const highlightMode = () => {
  mode.value = 2;
  pdfViewer.annotationEditorMode = { mode: pdfjsLib.AnnotationEditorType.HIGHLIGHT };
};

const freeTextMode = () => {
  mode.value = 3;
  pdfViewer.annotationEditorMode = { mode: pdfjsLib.AnnotationEditorType.FREETEXT };
}

onMounted(async () => {
  await loadPDF();
});

onUnmounted(() => {
  resizeObserver.disconnect();
});
</script>

<style>
/* patch to pdf.js */
.hidden,
[hidden] {
  display: none !important;
}
</style>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}
.pdfHost {
  position: relative;
  width: 100%;
  height: calc(100vh - 145px);
}
.viewerContainer {
  position: absolute;
  overflow: auto;
  width: 100%;
  height: 100%;
}
</style>
