<template>
    <div class="page">
      <argue :data="argueDataPending"></argue>
    </div>
</template>


<script setup lang="ts">
import argue from "../widgets/argue.vue"
import {useRoute} from "vue-router"

const { widgetId, submittedAssignmentId } = useRoute().query

const argueDataPending = {
  title: 'ArguePending',
  content: '# 要Argue的作业\n\n你觉得老师批改有误',
  attachments: [
    {filename: '您的提交.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
  ],
  status: 'pending',
  submitType: 'file',
  originalScore: 90,
  verifiedScore: 85,
  maxScore: 100,

  voteTotal: 0,
  voteSupport: 0,
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
