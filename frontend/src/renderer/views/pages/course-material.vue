<template>
  <div class="page">
    <doc :data="docData"></doc>
    <note-pdf :data="notePdfData"></note-pdf>
    <assignment :data="assignmentData"></assignment>
    <assignment :data="assignmentData2"></assignment>
    <assignment :data="assignmentData3"></assignment>
  </div>
</template>

<!--
  实现一个多功能的 Page ，可以以多种方式分享课程资料、上传作业、发放评分等。
  组件详见 @/views/widgets
-->

<script setup lang="ts">
import notePdf from "../widgets/notepdf.vue"
import doc from "../widgets/doc.vue"
import assignment from "../widgets/assignment.vue"

const notePdfData = {
  title: '互动式课件 [自定义title]',
  pdfFile: 'https://arxiv.org/pdf/2403.14740',
  notes: [
    {page: 1, x: 100, y: 100, text: "毕导：为什么开水和凉水听起来不一样"}
  ]
}

const docData = {
  title: '富文本文档 [自定义title]',
  content: '# 本项目 UI 组件为\n\n<img src=\"https://element-plus.org/images/element-plus-logo.svg\" width="75"\>',
  attachments: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.jpg', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.mp4', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.mp3', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.zip', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.tff', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
  ],
}

const assignmentData = {
  title: '作业 [自定义title]',
  content: '# 我是作业\n\n请完成作业',
  attachments: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
  ],
  status: 'pending',
  submitTypes: ['file', 'code'],
}

const assignmentData2 = {
  title: '已完成的作业',
  content: '# 我是作业\n\n请完成作业',
  attachments: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
  ],
  status: 'returned',
  submitTypes: ['file', 'code'],
  score: 90,
  maxScore: 100,
  feedback: 'ok',
  returned_files: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
  ],
}

const assignmentData3 = {
  title: '编辑提交记录',
  content: '# 我是作业\n\n请完成作业',
  attachments: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
  ],
  status: 'submitted',
  submitTypes: ['file', 'code'],
  submittedAssignment: [
    {
      content: "上次提交的文本",
      attachments: [
        {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
        {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      ],
      code: {
        content: "# 上次提交的代码",
        language: "python",
      },
      submittedTime: "2025-03-14 11:45:14",
    },
    {
      content: "上次提交的文本233",
      attachments: [
        {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
        {fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
      ],
      code: {
        content: "# 上次提交的代码",
        language: "python",
      },
      submittedTime: "2025-03-14 11:45:16",
    }
  ]
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