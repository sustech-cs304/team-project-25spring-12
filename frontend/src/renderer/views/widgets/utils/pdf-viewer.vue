<template>
  <el-card>
    <div class="mark-header" v-if="props.isMarking">
      <div style="text-align: center;">
        <el-button-group>
          <el-button
              v-for="(editorType, index) in editorTypes"
              :key="index"
              @click="changeEditorMode(editorType.mode)"
              :type="mode === editorType.mode ? 'primary' : ''"
          >
            {{ editorType.label }}
          </el-button>
        </el-button-group>
      </div>
      <div class="toolbar" v-show="mode === pdfjsLib.AnnotationEditorType.INK">
        <el-color-picker v-model="inkColor" @change="changeInkColor"/>
        <el-divider direction="vertical"/>
        <el-slider
            v-model="inkSize"
            :min="1"
            :max="20"
            :show-tooltip="false"
            style="width: 100px; display: inline-flex; margin-left: 10px;"
            @input="changeInkSize"
        />
      </div>
      <div class="toolbar" v-show="mode === pdfjsLib.AnnotationEditorType.HIGHLIGHT">
        <el-button
            circle
            v-for="(color, index) in highlightColors"
            :key="index"
            style="border-width: 2px;"
            :style="{ 'background-color': color}"
            :class="{focus: highlightDefaultColor === color}"
            @click="changeHighlightDefaultColor(color)"
        ></el-button>
      </div>
      <div class="toolbar" v-show="mode === pdfjsLib.AnnotationEditorType.FREETEXT">
        <el-color-picker v-model="textColor" @change="changeTextColor"/>
        <el-divider direction="vertical"/>
        <el-select v-model="textSize" @change="changeTextSize" style="width: 72px">
          <el-option
              v-for="size in textSizes"
              :key="size"
              :label="size"
              :value="size"
          />
        </el-select>
      </div>
      <el-divider />
    </div>
    <el-scrollbar
        ref="scrollbar"
        class="pdfScrollbar"
        style="z-index: 0;"
    ></el-scrollbar>
  </el-card>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref} from "vue";
import * as pdfjsLib from "pdfjs-dist";
import * as pdfjsViewer from "pdfjs-dist/web/pdf_viewer.mjs";
import pdfWorker from "pdfjs-dist/build/pdf.worker?url";
import "pdfjs-dist/web/pdf_viewer.css";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

const props = defineProps({
  pdfFile: {
    type: Object,
    required: true,
  },
  isMarking: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const highlightColors = {
  "yellow": "#FFFF98",
  "green": "#53FFBC",
  "blue": "#80EBFF",
  "pink": "#FFCBE6",
  "red": "#FF4F5F",
};

const textSizes = [8, 10, 12, 14, 18, 24, 36, 72];

const mode = ref(pdfjsLib.AnnotationEditorType.NONE);
const scrollbar = ref();
const inkColor = ref("#000000");
const inkSize = ref(1);
const highlightDefaultColor = ref(highlightColors.yellow);
const textColor = ref("#000000");
const textSize = ref(textSizes[2]);

let pdfViewer: pdfjsViewer.PDFViewer;
const eventBus = new pdfjsViewer.EventBus();
const resizeObserver = new ResizeObserver((entries) => {
  if (entries.length > 0) {
    pdfViewer.currentScaleValue = "page-width";
  }
});

const loadPDF = async () => {
  try {
    const container = scrollbar.value.wrapRef;
    container.classList.add("viewerContainer");
    const viewer = container.childNodes[0];
    viewer.classList.add("pdfViewer");
    pdfViewer = new pdfjsViewer.PDFViewer({
      container,
      viewer,
      eventBus,
      annotationEditorHighlightColors: Object.entries(highlightColors).map(([name, color]) => `${name}=${color}`).join(','),
    });
    eventBus.on("pagesinit", function () {
      pdfViewer.currentScaleValue = "page-width";
    });
    const loadingTask = pdfjsLib.getDocument(props.pdfFile.url);
    const pdfDocument = await loadingTask.promise;
    pdfViewer.setDocument(pdfDocument);
    resizeObserver.observe(container);
  } catch (e) {
    console.error(`Error rendering pdf:`, e);
  }
};

const editorTypes = [
  {label: "指针", mode: pdfjsLib.AnnotationEditorType.NONE},
  {label: "绘画", mode: pdfjsLib.AnnotationEditorType.INK},
  {label: "高亮", mode: pdfjsLib.AnnotationEditorType.HIGHLIGHT},
  {label: "文字", mode: pdfjsLib.AnnotationEditorType.FREETEXT},
];

const changeEditorMode = (value: number) => {
  mode.value = value;
  pdfViewer.annotationEditorMode = {mode: value};
};

const changeInkColor = (value: string) => {
  eventBus.dispatch("switchannotationeditorparams", {
    source: this,
    type: pdfjsLib.AnnotationEditorParamsType.INK_COLOR,
    value: value,
  });
};

const changeInkSize = (value: number) => {
  eventBus.dispatch("switchannotationeditorparams", {
    source: this,
    type: pdfjsLib.AnnotationEditorParamsType.INK_THICKNESS,
    value: value,
  });
};

const changeHighlightDefaultColor = (value: string) => {
  highlightDefaultColor.value = value;
  eventBus.dispatch("switchannotationeditorparams", {
    source: this,
    type: pdfjsLib.AnnotationEditorParamsType.HIGHLIGHT_DEFAULT_COLOR,
    value: value,
  });
};

const changeTextColor = (value: string) => {
  eventBus.dispatch("switchannotationeditorparams", {
    source: this,
    type: pdfjsLib.AnnotationEditorParamsType.FREETEXT_COLOR,
    value: value,
  });
};

const changeTextSize = (value: number) => {
  eventBus.dispatch("switchannotationeditorparams", {
    source: this,
    type: pdfjsLib.AnnotationEditorParamsType.FREETEXT_SIZE,
    value: value,
  });
};

onMounted(async () => {
  await loadPDF();
});

onUnmounted(() => {
  resizeObserver.disconnect();
});
</script>

<style scoped>
:deep(.el-card__header) {
  background-color: initial !important;
  padding: initial !important;
  margin: initial !important;
  border: initial !important;
}

:deep(.el-card__body) {
  background-color: initial !important;
  padding: initial !important;
  margin: initial !important;
}

.mark-header {
  padding-top: 15px;
  z-index: 1;
}

.toolbar {
  text-align: center;
  padding-top: 10px;
}

.focus {
  border-color: #409eff;
}

.pdfScrollbar {
  width: 100%;
  height: calc(100vh - 145px);
}

:deep(.viewerContainer) {
  position: absolute;
  width: 100%;
}

:deep(.hidden, [hidden]) {
  display: none !important;
}
</style>
