<template>
  <widget-card title="作业批改" color="blue" icon="Notebook">
    <div class="container">
      <!--   作业信息   -->
      <md-and-file-mark
          ref="submissionContainer"
          :submission-id="props.submission.id"
          :md-content="submission.content || ''"
          :file-list="submission.feedback?.attachments || submission.attachments"
          :download-file="props.downloadFile"
          @update-file="handleUpdateFile"
      />

      <!--   得分   -->
      <div class="assignment-status">
        <el-row class="status-row">
          <el-col :span="12" class="status-text">得分</el-col>
          <el-col :span="12" class="score-display">
            <el-input-number v-model="score" style="width: 72px" placeholder="分数" :controls="false" />
            <span> / {{ displayTotalScore }}</span>
          </el-col>
        </el-row>
      </div>
      <!--   评语   -->
      <div class="assignment-feedback">
        <el-row class="feedback-row">
          <el-col :span="24" class="feedback-text">评语</el-col>
          <el-col :span="24" class="feedback-input">
            <el-input
              type="textarea"
              v-model="content"
              placeholder="请输入评语"
              :rows="3"
            />
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="mark-submit">
      <el-tooltip
          :content="errorMessage"
          :disabled="errorMessage === null"
      >
        <el-button
            type="primary"
            :icon="Check"
            @click="handleSubmit"
            :disabled="errorMessage !== null"
            style="width: 120px; margin-left: auto"
        >
          提交
        </el-button>
      </el-tooltip>
    </div>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "./utils/widget-card.vue";
import MdAndFileMark from "./utils/md-and-file-mark.vue";
import {computed, ref, watch} from "vue";
import {Check} from "@element-plus/icons-vue";
import {FeedbackForm, SubmissionForMark} from "@/types/feedback";

const props = defineProps<{
  maxScore: number;
  submission: SubmissionForMark;
  feedback: FeedbackForm;
  downloadFile: (submissionId: number, fileId: string) => Promise<Blob>;
}>();

const emit = defineEmits<{
  (e: "updateFile", submissionId: number, fileId: string, dataPromise: Promise<Uint8Array>): void;
  (e: "save", submissionId: number, score: number, content: string): void;
  (e: "submit", submissionId: number, score: number, content: string): void;
}>();

const displayTotalScore = computed(() => props.maxScore);

const score = ref();
const content = ref("");
const submissionContainer = ref();

const errorMessage = computed(() => {
  if (score.value === undefined || score.value === null) return "请输入分数";
  if (score.value < 0 || score.value > props.maxScore) return "分数超出范围";
  return null;
});

const handleUpdateFile = (submissionId: number, fileId: string, dataPromise: Promise<Uint8Array>) => {
  emit("updateFile", submissionId, fileId, dataPromise);
};

const handleSubmit = () => {
  submissionContainer.value.save();
  emit("submit", props.submission.id, score.value, content.value);
};

watch([() => props.submission, () => props.feedback], ([newSubmission, newFeedback], [oldSubmission, oldFeedback]) => {
  if (oldSubmission) {
    if (submissionContainer.value.isDirty()) {
      submissionContainer.value.save();
    }
    emit("save", oldSubmission.id, score.value, content.value);
  }
  score.value = newFeedback.score;
  content.value = newFeedback.content || "";
}, {immediate: true});
</script>

<style scoped>
.container, .homework-submit {
  display: flex;
  flex-direction: column;
  padding: 0;
  background-color: transparent;
  border: none;
  gap: 15px;
}

.mark-submit {
  display: flex;
  flex-direction: column;
  padding: 0;
  margin-top: 10px;
  background-color: transparent;
  border: none;
  gap: 15px;
}

.assignment-status, .assignment-feedback {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  background: #f9fafb;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  padding: 15px;
}

.status-row, .feedback-row {
  width: 100%;
}

.status-text, .feedback-text {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 8px;
}

.feedback-input {
  width: 100%;
}

.el-input {
  width: 100%;
  font-size: 14px;
}

.score-display {
  text-align: right;
}
</style>
