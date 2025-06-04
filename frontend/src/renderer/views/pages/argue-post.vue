<template>
    <div class="page">
      <!-- <argue :data="argueDataPending"></argue> -->
      <argue :data="argueDataSubmitted"></argue>
      <argue :data="argueDataReturned"></argue>
    </div>
</template>


<script setup lang="ts">
import { onMounted, ref } from "vue"
import { ElMessage } from "element-plus"
import argue from "../widgets/argue.vue"
import service from '../../utils/request';
import {useRoute} from "vue-router"

const argueData = ref({})
const argueId = ref(0);

const argueDataSubmitted = ref({
  title: 'ArgueSubmitted',
  content: '# 要Argue的作业\n\n你觉得老师批改有误',
  attachments: [
    {filename: '您的提交.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
  ],
  status: 'submitted',
  submitType: 'file',
  originalScore: 90,
  revisedScore: 85,
  maxScore: 100,

  submittedArguement: {
      attachments: [
        {
          filename: '您的争辩附件.pdf',
          url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip',
        },
      ],
      content: "# This is my kingdom come↑\n\nThis is my kingdom come↓",
      time: "2025-03-14 11:45:16",
  },

  voteTotal: 0,
  voteSupport: 0,

  comments: [],

})

const argueDataReturned = ref({
  title: 'ArgueReturned',
  content: '# 要Argue的作业\n\n你觉得老师批改有误',
  status: 'returned',
  submitType: 'file',
  originalScore: 90,
  revisedScore: 85,
  maxScore: 100,

  voteTotal: 0,
  voteSupport: 0,

  comments: [],
})

onMounted(async () => {
  try {
    argueId.value = Number(useRoute().params.argueId);
    const response = await service.get(`/argue/${argueId}`);
  } catch (error) {
    ElMessage.error("加载争辩数据失败，请稍后重试")
  }
})
</script>


<style scoped>
  .page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
</style>
