<template>
  <widget-card title="作业批改" color="blue" icon="Notebook">
    <div class="container">
      <!--   作业信息   -->
      <md-and-file-mark
          ref="submissionContainer"
          :submission-id="props.submission.id"
          :md-content="submission.content || ''"
          :file-list="submission.feedback?.attachments || submission.attachments"
          :get-file="handleGetFile"
          @update-file="handleUpdateFile"
      />

      <!--   得分   -->
      <div class="assignment-status">
        <el-row class="status-row">
          <el-col :span="12" class="status-text">得分</el-col>
          <el-col :span="12" class="score-display">
            <el-input-number v-model="score" style="width: 72px" placeholder="分数" :controls="false"/>
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
    <el-row class="mark-submit" :gutter="15">
      <el-col :span="12">
        <el-button
            :icon="MagicStick"
            @click="handleOpenDialog"
            style="width: 120px; margin-left: auto"
        >
          AI 辅助评分
        </el-button>
      </el-col>
      <el-col :span="12" style="text-align: right">
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
      </el-col>
    </el-row>
  </widget-card>

  <el-dialog
      v-model="dialogVisible"
      title="AI 辅助评分"
  >
    <el-form ref="formEl" :model="dialogForm" :rules="rules" label-width="auto">
      <el-form-item prop="type" label="类型">
        <el-radio-group v-model="dialogForm.type">
          <el-radio value="text">文本</el-radio>
          <el-radio value="pdf">PDF</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item prop="question" label="问题" v-if="dialogForm.type === 'text'">
        <el-input
            type="textarea"
            v-model="dialogForm.question"
            placeholder="请输入问题"
            :rows="3"
        />
      </el-form-item>
      <el-form-item prop="questionFileId" label="问题" v-else>
        <el-select v-model="dialogForm.questionFileId" placeholder="选择题目附件">
          <el-option
              v-for="item in questionPDFs"
              :key="item.id"
              :label="item.filename"
              :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item prop="answer" label="参考答案" v-if="dialogForm.type === 'text'">
        <el-input
            type="textarea"
            v-model="dialogForm.answer"
            placeholder="请输入参考答案"
            :rows="3"
        />
      </el-form-item>
      <el-form-item prop="answerFileId" label="参考答案" v-else>
        <el-upload
            ref="uploadContainer"
            :http-request="handleUpload"
            :limit="1"
            :on-exceed="handleExceed"
            :on-remove="handleRemove"
        >
          <el-button :icon="Upload">上传答案 PDF</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item prop="studentAnswer" label="学生回答" v-if="dialogForm.type === 'text'">
        <el-input
            type="textarea"
            v-model="dialogForm.studentAnswer"
            placeholder="请输入学生回答"
            :rows="3"
        />
      </el-form-item>
      <el-form-item prop="studentAnswerFileId" label="学生回答" v-else>
        <el-select v-model="dialogForm.studentAnswerFileId" placeholder="选择回答附件">
          <el-option
              v-for="item in studentAnswerPDFs"
              :key="item.id"
              :label="item.filename"
              :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item prop="prompt" label="额外 Prompt">
        <el-input
            type="textarea"
            v-model="dialogForm.prompt"
            placeholder="请输入额外 prompt"
            :rows="3"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleAISubmit" :disabled="isAISubmitting">确认</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import WidgetCard from "./utils/widget-card.vue";
import MdAndFileMark from "./utils/md-and-file-mark.vue";
import {computed, reactive, ref, watch} from "vue";
import {Check, MagicStick, Upload} from "@element-plus/icons-vue";
import {FeedbackForm, SubmissionForMark} from "@/types/feedback";
import {AssignmentWidget} from "@/types/widgets";
import {
  ElMessage,
  FormInstance, FormRules,
  genFileId,
  UploadInstance,
  UploadProps,
  UploadRawFile,
  UploadRequestOptions
} from "element-plus";
import {useUploader} from "@/composables/useUploader";
import {AIFeedbackCreate, postAIFeedback} from "@/api/feedback";

const props = defineProps<{
  assignmentWidget: AssignmentWidget;
  submission: SubmissionForMark;
  feedback: FeedbackForm;
  blobList: Record<string, Blob>;
  patch: Record<string, Uint8Array>;
}>();

const emit = defineEmits<{
  (e: "updateFile", fileId: string, dataPromise: Promise<Uint8Array>): void;
  (e: "save", submissionId: number, score: number, content: string): void;
  (e: "submit", submissionId: number, score: number, content: string): void;
}>();

const {upload} = useUploader();

const displayTotalScore = computed(() => props.assignmentWidget.maxScore);
const questionPDFs = computed(() => props.assignmentWidget.attachments.filter(a => a.filename.endsWith(".pdf")));
const studentAnswerPDFs = computed(() => (props.submission.attachments?.filter(a => a.filename.endsWith(".pdf")) || []));

const score = ref<number>();
const content = ref("");
const submissionContainer = ref<InstanceType<typeof MdAndFileMark>>();
const dialogVisible = ref(false);
const formEl = ref<FormInstance>();
const dialogForm = reactive<AIFeedbackCreate>({
  type: "text",
  question: "",
  answer: "",
  studentAnswer: "",
  questionFileId: "",
  answerFileId: "",
  studentAnswerFileId: "",
  maxScore: 100,
  prompt: "",
});
const uploadContainer = ref<UploadInstance>();
const isAISubmitting = ref(false);

const notEmpty = (rule: any, value: any, callback: any) => {
  if (dialogForm.type === "text" || !!value) {
    callback();
  } else {
    callback(new Error("请选择文件"));
  }
}
const rules = reactive<FormRules<typeof dialogForm>>({
  questionFileId: [{ validator: notEmpty }],
  answerFileId: [{ validator: notEmpty }],
  studentAnswerFileId: [{ validator: notEmpty }],
});

const errorMessage = computed(() => {
  if (score.value === undefined || score.value === null) return "请输入分数";
  if (score.value < 0 || score.value > props.assignmentWidget.maxScore) return "分数超出范围";
  if (!isDirty() && !isPatchDirty() && !submissionContainer.value?.isDirty()) return "当前内容已提交";
  return null;
});

const handleGetFile = (fileId: string) => {
  if (fileId in props.patch)
    return new Blob([props.patch[fileId]]);
  return props.blobList[fileId];
};

const handleUpdateFile = (fileId: string, dataPromise: Promise<Uint8Array>) => {
  emit("updateFile", fileId, dataPromise);
};

const handleSubmit = () => {
  submissionContainer.value?.save();
  if (score.value !== undefined) {
    emit("submit", props.submission.id, score.value, content.value);
  }
};

const handleOpenDialog = () => {
  dialogForm.studentAnswer = props.submission.content || "";
  dialogVisible.value = true;
}

const handleExceed: UploadProps['onExceed'] = (files) => {
  uploadContainer.value!.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  uploadContainer.value!.handleStart(file);
  uploadContainer.value!.submit();
};

const handleRemove: UploadProps['onRemove'] = () => {
  dialogForm.answerFileId = "";
}

const handleUpload = async (options: UploadRequestOptions) => {
  const {file, onSuccess, onError} = options;
  try {
    const result = await upload(file);
    dialogForm.answerFileId = result.id;
    onSuccess(result);
  } catch (err: any) {
    ElMessage.error("上传失败，请稍后重试");
    onError(err);
  }
};

const handleAISubmit = () => {
  if (!formEl.value) {
    return;
  }
  formEl.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        isAISubmitting.value = true;
        const response = await postAIFeedback(dialogForm);
        score.value = response.data.score;
        content.value = response.data.feedback;
        dialogVisible.value = false;
      } catch (e) {
        ElMessage.error("提交失败，请稍后重试");
      } finally {
        isAISubmitting.value = false;
      }
    }
  });
};

const isDirty = () => {
  return score.value !== props.feedback.score || content.value !== (props.feedback.content || "");
};

const isPatchDirty = () => {
  const files = props.submission.feedback?.attachments || props.submission.attachments;
  return files?.some(file => file.id in props.patch) ?? false;
};

watch([() => props.submission, () => props.feedback], ([newSubmission, newFeedback], [oldSubmission, oldFeedback]) => {
  if (oldSubmission) {
    if (submissionContainer.value?.isDirty()) {
      submissionContainer.value.save();
    }
    if (score.value !== undefined) {
      emit("save", oldSubmission.id, score.value, content.value);
    }
  }
  score.value = newFeedback.score;
  content.value = newFeedback.content || "";
  dialogForm.question = props.assignmentWidget.content;
  dialogForm.maxScore = props.assignmentWidget.maxScore;
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
  flex-direction: row;
  padding: 0;
  margin-top: 10px;
  background-color: transparent;
  border: none;
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
