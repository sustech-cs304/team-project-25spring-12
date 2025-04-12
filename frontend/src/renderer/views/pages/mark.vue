<template>
  <div class="page">
    <assignment-mark :data="assignmentMarkData"></assignment-mark>
  </div>
</template>

<script setup lang="ts" name="mark">
import assignmentMark from "../widgets/assignment-mark.vue";
const assignmentMarkData = {
  title: '作业批改',
  content: '# 我是作业\n\n请完成作业',
  attachments: [
    {fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe'},
    {fileName: '为什么开水和凉水听起来不一样.pdf', url: 'https://arxiv.org/pdf/2403.14740'},
    {fileName: 'index.txt', url: 'https://raw.githubusercontent.com/xz-xuezhe/sample/refs/heads/master/index.html'},
    {fileName: 'hello.md', url: 'https://raw.githubusercontent.com/xz-xuezhe/sample/refs/heads/master/hello.md'},
    {fileName: 'element-plus-logo.jpg', url: 'https://element-plus.org/images/element-plus-logo.svg'},
    {fileName: 'ギターと孤独と蒼い惑星.mp3', url: 'https://music.163.com/song/media/outer/url?id=2024541857.mp3'},
    {fileName: '1280*720 from sample-video.com.mp4', url: 'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4'},
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