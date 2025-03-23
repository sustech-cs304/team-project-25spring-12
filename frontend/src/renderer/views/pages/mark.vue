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
      <div ref="host"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import * as pdfjsLib from "pdfjs-dist";
import * as pdfjsViewer from "pdfjs-dist/web/pdf_viewer.mjs";
import pdfWorker from "pdfjs-dist/build/pdf.worker?url";
import cssUrl from "pdfjs-dist/web/pdf_viewer.css?url";
import "pdfjs-dist/web/pdf_viewer.css";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const props = {
  data: {
    pdfFile: 'https://arxiv.org/pdf/2403.14740',
  },
};

const mode = ref(0);
const host = ref();
var pdfViewer: pdfjsViewer.PDFViewer;
var resizeObserver: ResizeObserver;

const getShadow = () => {
  if (!host.value) {
    console.error("host div is not mounted");
  }

  const root = host.value.attachShadow({ mode: "open" });

  const link = document.createElement("link");
  link.href = cssUrl;
  link.rel = "stylesheet";
  root.appendChild(link);

  const container = document.createElement("div");
  container.style.position = "absolute";
  container.style.overflow = "auto";
  container.style.height = "calc(100vh - 145px)";
  container.style.width = "100%";
  root.appendChild(container);

  const viewer = document.createElement("div");
  viewer.id = "viewer";
  viewer.classList.add("pdfViewer");
  container.appendChild(viewer);

  return container;
};

const loadPDF = async () => {
  try {
    const container = getShadow();
    const eventBus = new pdfjsViewer.EventBus();
    const viewer = new pdfjsViewer.PDFViewer({
      container,
      eventBus,
      annotationEditorHighlightColors: '#ffff98',
    });
    eventBus.on("pagesinit", function () {
      viewer.currentScaleValue = "page-width";
    })
    const loadingTask = pdfjsLib.getDocument(props.data.pdfFile);
    const pdfDocument = await loadingTask.promise;
    viewer.setDocument(pdfDocument);
    const observer = new ResizeObserver((entries) => {
      if (entries) {
        viewer.currentScaleValue = "page-width";
      }
    });
    observer.observe(container);
    pdfViewer = viewer;
    resizeObserver = observer;
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
