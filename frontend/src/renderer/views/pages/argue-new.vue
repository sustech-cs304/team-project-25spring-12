<template>
    <div class="page" v-if="childready">
      <argue :data="argueNew"></argue>
    </div>
</template>


<script setup lang="ts">
import { onMounted, ref } from "vue"
import argue from "../widgets/argue.vue"
import {useRoute} from "vue-router"
import request from '../../utils/request';
import { useUserStore } from "../../store/user";

const childready = ref(false)
const { widgetId } = useRoute().query
const userStore = useUserStore();

const argueNew = ref({})

onMounted(async () => {
  try {
    const response = await request.get(`/class/widget/${widgetId}/submission/student`);
    // const assignmentContent = response.data.content;
    // const assignmentFileList = response.data.attachments;
    const submission = response.data.submittedAssignment.at(-1);
    // const submissionContent = submission.content;
    // const submissionFileList = submission.attachments;
    // const feedbackContent = submission.feedback.content;
    // const feedbackFileList = submission.feedback.attachments;

    argueNew.value = {
      argueId: -1,

      widgetId: widgetId,
      submittedAssignmentId: submission.id,
      title: "",

      status: "pending",
      assignmentContent: response.data.content || "",
      assignmentFileList: response.data.attachments || [],
      submissionContent: submission.content || "",
      submissionFileList: submission.attachments || [],
      feedbackContent: submission.feedback.content || "",
      feedbackFileList: submission.feedback.attachments || [],

      originalScore: submission.feedback.score,
      maxScore: response.data.maxScore,
      revisedScore: 0,
      
      submitTime: "",

      argueContent: "",
      argueFileList: [],
      argueFeedbackContent: "",
      argueFeedbackFileList: [],

      voteSupport: 0,
      voteTotal: 0,
      
    }
    console.log("newdata: ", argueNew.value);
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
