<template>
  <widget-card :title="computedTitle" color="green" icon="Document">
    <div class="container">
      <md-preview :id="id" v-bind="editorProps" />
      <MdCatalog :editorId="id" :scrollElement="scrollElement" />
    </div>
<!--    here-->
  </widget-card>
</template>

<script setup lang="ts">
import {computed, defineProps} from 'vue';
import { MdPreview } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import widgetCard from "./widget-card.vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const id = 'preview-only';
const scrollElement = document.documentElement;

const computedTitle = computed(() => {
  return props.data?.title || "富文本展示区";
});

const editorProps = {
  modelValue: props.data.content,
  readOnly: true,
  toolbars: [],
  footers: [],
};
</script>