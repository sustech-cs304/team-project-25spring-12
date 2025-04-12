<template>
  <widget-card :title="computedTitle" color="blue" icon="Notebook">
    <div class="container">
      <!--   作业信息   -->
      <md-and-file :data="props.data" v-if="props.data.status !== 'marking'"/>
      <md-and-file-mark :data="props.data" v-else/>

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
            :disabled="error || score === undefined"
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
const error = ref(false);

watch(score, (newVal) => {
  error.value = newVal < 0 || newVal > props.data.maxScore;
});

const errorMessage = computed(() => {
  if (score.value === undefined) return "请输入分数";
  if (error.value) return "分数超出范围";
  return "";
});

const submit = () => {
  // TODO: 上传分数
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

.toolbar {
  display: flex;
  align-items: center;
  gap: 15px;
  background-color: white;
  width: 100%;
  padding: 10px;
}

.code-editor {
  display: flex;
  flex-direction: column;
  height: 700px;
  overflow: hidden;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.code-editor :deep(.CodeMirror) {
  height: 100%;
}

.el-text {
  margin-right: 8px;
  font-size: 14px;
  color: #606266;
}

.el-select {
  width: 120px;
  margin-right: 20px;
}

.assignment-status {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f9fafb;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  padding: 0 15px;
}

.status-row {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-text {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: 500;
}

.status-icon {
  margin-right: 8px;
}

.score-display {
  text-align: right;
  font-weight: bold;
}

.score {
  font-size: 22px;
  font-weight: 700;
}

.total-score {
  font-size: 16px;
  color: #666;
}

.submit-record {
  min-width: 350px;
  background: #f9fafb;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.submit-record-title {
  font-weight: bold;
  font-size: 18px;
  color: #333;
}

.submit-record-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.submit-record-item:hover {
  background: #f1f1f1;
}

.edit-button {
  text-align: right;
}

.el-button {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
}

.el-button:hover {
  background-color: #66b1ff;
}
</style>
