<template>
    <div class="page">
      <argue :data="argueDataPending"></argue>
      <argue :data="argueDataSubmitted"></argue>
      <argue :data="argueDataReturned"></argue>
    </div>
</template>


<script setup lang="ts">
  import argue from "../widgets/argue.vue"
  
  const argueDataPending = {
    title: 'ArguePending',
    content: '# 要Argue的作业\n\n你觉得老师批改有误',
    attachments: [
      {fileName: '您的提交.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
    ],
    status: 'pending',
    submitTypes: ['file'],
    originalScore: 90,
    verifiedScore: 85,
    maxScore: 100,

    voteTotal: 0,
    voteSupport: 0,
  }

  const argueDataSubmitted = {
    title: 'ArgueSubmitted',
    content: '# 要Argue的作业\n\n你觉得老师批改有误',
    attachments: [
      {
        fileName: '您的提交.pdf',
        url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip',
      },
    ],
    status: 'submitted',
    submitTypes: ['file'],
    originalScore: 90,
    verifiedScore: 85,
    maxScore: 100,
    
    submittedArguement: {
        attachments: [
          {
            fileName: '您的争辩附件.pdf',
            url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip',
          },
        ],
        content: "# This is my kingdom come↑\n\nThis is my kingdom come↓",
        time: "2025-03-14 11:45:16",
    },

    voteTotal: 0,
    voteSupport: 0,
  }

  const argueDataReturned = {
    title: 'ArgueReturned',
    content: '# 要Argue的作业\n\n你觉得老师批改有误',
    attachments: [
      {fileName: '您的提交.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
    ],
    status: 'returned',
    submitTypes: ['file'],
    originalScore: 90,
    verifiedScore: 85,
    maxScore: 100,

    submittedArguement: {
        attachments: [
          {
            fileName: '您的争辩附件.pdf',
            url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip',
          },
        ],
        content: "# This is my kingdom come↑\n\nThis is my kingdom come↓",
        time: "2025-03-14 11:45:16",
    },

    voteTotal: 3,
    voteSupport: 1,
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
