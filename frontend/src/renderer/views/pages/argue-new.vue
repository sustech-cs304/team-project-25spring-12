<template>
    <div class="page">
      <argue :data="argueNew"></argue>
    </div>
</template>


<script setup lang="ts">
import { onMounted, ref } from "vue"
import argue from "../widgets/argue.vue"
import {useRoute} from "vue-router"
import request from '../../utils/request';

const { widgetId } = useRoute().query

const argueNew = ref({})

onMounted(async () => {
  try {
    const response = await request.get(`/class/widget/${widgetId}/submission/student`);
    console.log("newdata: ", response.data);
    // const assignmentContent = response.data.content;
    // const assignmentFileList = response.data.attachments;
    const submission = response.data.submittedAssignment.at(-1);
    console.log("sub: ", submission);
    // const submissionContent = submission.content;
    // const submissionFileList = submission.attachments;
    // const feedbackContent = submission.feedback.content;
    // const feedbackFileList = submission.feedback.attachments;
    argueNew.value = {
      status: "pending",
      assignmentContent: response.data.content || "",
      assignmentFileList: response.data.attachments || [],
      submissionContent: submission.content || "",
      submissionFileList: submission.attachments || [],
      feedbackContent: submission.feedback.content || "",
      feedbackFileList: submission.feedback.attachments || [],
      argueContent: "",
      argueFileList: [],
      argueFeedbackContent: "",
      argueFeedbackFileList: [],
      submitTime: "",
    }
    console.log("newdata: ", argueNew.value);
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
