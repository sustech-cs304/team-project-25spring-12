<template>
  <div ref="editorContainer" style="height: 100%; width: 100%;"></div>
</template>

<script setup lang="ts">
import {ref, watch, onMounted} from "vue";
import * as monaco from "monaco-editor";

const props = defineProps({
  language: {
    type: String,
    required: true,
  },
  code: {
    type: String,
    required: true,
  }
});

const editorContainer = ref<HTMLDivElement | null>(null);
let editorInstance: monaco.editor.IStandaloneCodeEditor | null = null;

onMounted(() => {
  if (editorContainer.value) {
    editorInstance = monaco.editor.create(editorContainer.value, {
      value: props.code,
      language: props.language,
      theme: "vs-dark",
    });

    editorInstance?.layout();
  }

  window.addEventListener("resize", () => {
    editorInstance?.layout();
  });
});

watch(() => props.language, (newLang) => {
  if (editorInstance) {
    monaco.editor.setModelLanguage(editorInstance.getModel()!, newLang);
  }
});

watch(() => props.code, (initCode) => {
  if (editorInstance) {
    editorInstance.setValue(initCode);
  }
});

defineExpose({
  getCode: () => editorInstance?.getValue() || "",
});
</script>
