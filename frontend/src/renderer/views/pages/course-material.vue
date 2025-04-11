<template>
  <div class="page">
    <DynamicWidget v-for="widget in widgets" :key="widget.id" :data="widget" />
  </div>
</template>

<script setup lang="ts">
import type { WidgetUnion } from '@/types/widgets';
import DynamicWidget from '@/views/widgets/dynamic-widget.vue';

const widgets: WidgetUnion[] = [  // TODO: 从后端获取
  {
    id: '1',
    index: 1,
    type: 'notepdf',
    title: '互动式课件 [自定义title]',
    createTime: '2025-03-01T12:00:00Z',
    updateTime: '2025-03-02T12:00:00Z',
    visible: true,
    editor: null,
    pdfFile: {
      fileName: '为什么开水和凉水听起来不一样.pdf',
      url: 'https://arxiv.org/pdf/2403.14740',
    },
    notes: [
      { page: 1, x: 100, y: 100, text: '毕导：为什么开水和凉水听起来不一样' },
    ],
  },
  {
    id: '2',
    index: 2,
    type: 'doc',
    title: '富文本文档 [自定义title]',
    createTime: '2025-03-01T12:00:00Z',
    updateTime: '2025-03-02T12:00:00Z',
    visible: true,
    editor: null,
    content: '# 本项目 UI 组件为\n\n<img src="https://element-plus.org/images/element-plus-logo.svg" width="75"/>',
    attachments: [
      { fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe' },
      { fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe' },
    ],
  },
  {
    id: '3',
    index: 3,
    type: 'assignment',
    title: '作业 [自定义title]',
    createTime: '2025-03-01T12:00:00Z',
    updateTime: '2025-03-02T12:00:00Z',
    visible: true,
    argueId: 0,
    editor: null,
    content: '# 我是作业\n\n请完成作业',
    attachments: [
      { fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe' },
    ],
    submitTypes: ['file', 'code'],
    submittedAssignment: null,
    status: 'pending',
  },
];
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>