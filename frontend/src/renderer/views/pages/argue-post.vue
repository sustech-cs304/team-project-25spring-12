<template>
    <div class="page" v-if="childready">
      <argue :data="arguePost"></argue>
    </div>
</template>


<script setup lang="ts">
import { onMounted, ref } from "vue"
import argue from "../widgets/argue.vue"
import {useRoute} from "vue-router"
import request from '../../utils/request';
import { useUserStore } from "../../store/user";

const childready = ref(false)
const argueId = useRoute().params.argueId
const userStore = useUserStore();

const arguePost = ref({})

onMounted(async () => {
  try {
    const response = await request.get(`/argue/${argueId}`);
    console.log("response", response.data);

    const submission = response.data.assignment.submittedAssignment[0]
    console.log("submossion", submission)

    let argueFeedback = {
        score: -1,
        content: "",
        fileList: [],
      }
    if (response.data.feadback) {
      argueFeedback = {
        score: response.data.feedback.score,
        content: response.data.feedback.content,
        fileList: response.data.feedback.attachments,
      }
    }

    arguePost.value = {
      argueId: argueId,

      widgetId: response.data.widgetId,
      submittedAssignmentId: response.data.submittedAssignmentId,
      title: "",
      
      status: response.data.status,
      assignmentContent: response.data.assignment.content || "",
      assignmentFileList: response.data.assignment.attachments || [],
      submissionContent: submission.content || "",
      submissionFileList: submission.attachments || [],
      feedbackContent: submission.feedback.content || "",
      feedbackFileList: submission.feedback.attachments || [],
      argueFeedbackContent: argueFeedback.content || "",
      argueFeedbackFileList: argueFeedback.fileList || [],

      submitTime: response.data.createTime,
      argueContent: response.data.content,
      argueFileList: response.data.attachments,

      originalScore: response.data.oldScore,
      maxScore: response.data.assignment.maxScore,
      revisedScore: argueFeedback.score,

      voteSupport: response.data.support,
      voteTotal: response.data.support + response.data.notSupport,
      
      isVoted: response.data.isVoted,
      isFollowed: response.data.isFollowed,

      comments: response.data.comments,
    }
    console.log("postdata: ", arguePost.value);
    childready.value = true;
  } catch (error) {
    
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
