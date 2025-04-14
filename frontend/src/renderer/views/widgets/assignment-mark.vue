<template>
  <widget-card :title="computedTitle" color="blue" icon="Notebook">
    <div class="container">
      <!--   作业信息   -->
      <md-and-file-mark :data="props.data"/>

      <!--   得分   -->
      <div class="assignment-status">
        <el-row class="status-row">
          <el-col :span="12" class="status-text">得分</el-col>
          <el-col :span="12" class="score-display">
            <el-input-number v-model="score" style="width: 72px" placeholder="分数" :controls="false"></el-input-number>
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
              v-model="feedback"
              placeholder="请输入评语"
              :maxlength="200"
              show-word-limit
              rows="3"
            ></el-input>
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="mark-submit">
      <el-tooltip
          :content="errorMessage"
          :disabled="errorMessage === ''"
      >
        <el-button
            type="primary"
            :icon="Check"
            @click="submit"
            :disabled="error || score === undefined || score === null"
            style="width: 120px; margin-left: auto"
        >
          确认
        </el-button>
      </el-tooltip>
    </div>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "./utils/widget-card.vue";
import MdAndFile from "./utils/md-and-file.vue";
import MdAndFileMark from "./utils/md-and-file-mark.vue";
import {computed, onMounted, ref, watch} from "vue";
import {Check, Close} from "@element-plus/icons-vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

// 本卡片的标题
const computedTitle = computed(() => props.data?.title || "作业");

const displayTotalScore = computed(() => (props.data.status === "marking" || props.data.status === "returned" ? props.data.maxScore : "--"));

const score = ref();
const feedback = ref("");
const error = ref(false);

watch(score, (newVal) => {
  console.log(newVal);
  error.value = newVal < 0 || newVal > props.data.maxScore;
});

const errorMessage = computed(() => {
  if (score.value === undefined || score.value === null) return "请输入分数";
  if (error.value) return "分数超出范围";
  return "";
});

const submit = () => {
  // TODO: 上传分数和评语
  console.log("分数:", score.value);
  console.log("评语:", feedback.value);
};
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
