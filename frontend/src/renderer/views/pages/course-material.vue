<template>
  <div class="page">
    <doc :data="docData"></doc>
    <note-pdf :data="notePdfData"></note-pdf>
  </div>
</template>

<script setup lang="ts">
  import notePdf from "../element/widgets/notepdf.vue"
  import doc from "../element/widgets/doc.vue"

  const notePdfData = {
    title: '互动式课件 [自定义title]',
    pdf_file: 'https://arxiv.org/pdf/2403.14740',
    notes: [
      {page: 1, x: 100, y: 100, text: "毕导：为什么开水和凉水听起来不一样"}
    ]
  }

  const docData = {
    title: '富文本文档 [自定义title]',
    content: '# 本项目 UI 组件为\n\n<img src=\"https://element-plus.org/images/element-plus-logo.svg\" width="75"\>',
    attachments: [
      {file_name: '真7zip.exe', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      {file_name: '伪7zip.pdf', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      {file_name: '伪7zip.jpg', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      {file_name: '伪7zip.mp4', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      {file_name: '伪7zip.mp3', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      {file_name: '伪7zip.zip', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      {file_name: '伪7zip.tff', URL: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    ],
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