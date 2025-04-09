<template>
    <div class="page">
      <assignment :data="assignmentData"></assignment>
      <argue :data="argueData"></argue>
    </div>
  </template>
  
  <script setup lang="ts">
  import assignment from "../widgets/assignment.vue"
  import argue from "../widgets/argue.vue"
  
  const assignmentData = {
    title: 'Assignment',
    content: '# 芝士作业\n\n请完成',
    attachments: [
      {fileName: '附件.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
    ],
    status: 'returned',
    submitTypes: ['file', 'code'],
    score: 90,
    maxScore: 100,
  }

  const argueData = {
    title: 'Argue',
    content: '# 要Argue的作业\n\n你觉得老师批改有误',
    attachments: [
      {fileName: '您的提交.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
    ],
    status: 'returned',
    submitTypes: ['file'],
    originalScore: 90,
    verifiedScore: 70,
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