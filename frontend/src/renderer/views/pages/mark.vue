<template>
  <div class="page">
    <assignment-mark :data="assignmentMarkData"></assignment-mark>
  </div>
</template>

<script setup lang="ts">
import assignmentMark from "../widgets/assignment-mark.vue";
const assignmentMarkData = {
  title: '作业批改',
  content: '# 我是作业\n\n请完成作业',
  attachments: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '为什么开水和凉水听起来不一样.pdf', url: 'https://arxiv.org/pdf/2403.14740'},
  ],
  status: 'marking',
  submitTypes: ['file', 'code'],
  maxScore: 100,
}
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}
</style>