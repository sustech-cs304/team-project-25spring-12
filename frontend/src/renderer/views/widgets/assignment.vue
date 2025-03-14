<template>
  <widget-card :title="computedTitle" color="orange" icon="Notebook">
    <div class="container">
      <!--   作业状态   -->
      <div class="assignment-status">
        <el-row class="status-row">
          <!-- 状态信息 -->
          <el-col :span="12" class="status-text">
            <el-icon :size="28" class="status-icon" :color="statusColor">
              <component :is="statusIcon"/>
            </el-icon>
            <el-text>
              {{ statusText }}
            </el-text>
          </el-col>

          <!-- 得分展示 -->
          <el-col :span="12" class="score-display">
            <span class="score" :style="{ color: scoreColor }">{{ displayScore }}</span>
            <span class="total-score"> / {{ displayTotalScore }}</span>
          </el-col>
        </el-row>
      </div>

      <!--   作业信息   -->
      <md-and-file :data="props.data"/>

      <!--   作业信息   -->
      <div class="submit-record" v-if="props.data.status === 'submitted'">
        <el-row justify="space-between">
          <el-text size="large" class="submit-record-title"> 提交记录</el-text>
        </el-row>
        <el-divider></el-divider>
        <el-row
            v-for="record in props.data.submitted_assignment"
            :key="record.submitted_time"
            class="submit-record-item"
            justify="space-between"
        >
          <el-col :span="1">
            <el-icon :size="20">
              <component :is="Memo"/>
            </el-icon>
          </el-col>
          <el-col :span="16">
            <el-text truncated> 提交时间：{{ record.submitted_time }}</el-text>
          </el-col>
          <el-col :span="6" class="edit-button">
            <el-button
                type="primary"
                link
                :icon="Edit"
                @click="editSubmittedAssignment(record?.content, record?.code, record?.attachments)"
            >
              编辑
            </el-button>
          </el-col>
        </el-row>
      </div>

      <!--   提交作业区   -->
      <div class="homework-submit" v-if="props.data.status === 'pending' || isEditing">
        <div class="code-editor" v-if="props.data.submit_types.includes('code')">
          <div class="toolbar">
            <span class="el-text">选择语言：</span>
            <el-select v-model="selectedLanguage" size="small" @change="updateMode">
              <el-option v-for="lang in languages" :key="lang.value" :label="lang.label" :value="lang.value"/>
            </el-select>

            <span class="el-text">Tab 长度：</span>
            <el-select v-model="tabSize" placeholder="Tab 长度" size="small">
              <el-option v-for="size in tabSizes" :key="size" :label="`${size} 空格`" :value="size"/>
            </el-select>

            <el-button type="primary" :icon="Upload" @click="submitCode" class="submit-btn">提交</el-button>
          </div>

          <div id="code-editor" style="height: 100%"></div>

        </div>

        <div class="homework-editor" v-if="props.data.submit_types.includes('file')">
          <md-and-file-editor :text="editingText" :file_list="editingFileList"/>
        </div>
      </div>

    </div>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "./utils/widget-card.vue";
import MdAndFile from "./utils/md-and-file.vue";
import MdAndFileEditor from "./utils/md-and-file-editor.vue";
import {computed, ref} from "vue";
import {Checked, Edit, Finished, Memo, Timer, Upload} from "@element-plus/icons-vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const value = /* set from `myEditor.getModel()`: */ `function hello() {
	alert('Hello world!');
}`;

// Hover on each property to see its docs!
const myEditor = monaco.editor.create(document.getElementById("code-editor"), {
  value,
  language: "javascript",
  automaticLayout: true,
});


const languages = [
  {label: "C++", value: "text/x-c++src"},
  {label: "Java", value: "text/x-java"},
  {label: "Python", value: "python"},
];

const computedTitle = computed(() => props.data?.title || "作业");

const code = ref("");
const selectedLanguage = ref("text/x-c++src");
const tabSizes = [2, 4, 8];
const tabSize = ref(4);

const options = computed(() => ({
  mode: selectedLanguage.value,
  theme: "dracula",
  lineNumbers: true,
  tabSize: tabSize.value,
  indentUnit: tabSize.value,
  indentWithTabs: true,
  autoCloseBrackets: true,
}));

const updateMode = () => {
  options.value.mode = selectedLanguage.value;
};

const submitCode = () => {
  console.log(code.value);
  // TODO: 上传到后端
};

const statusIcon = computed(() => {
  if (props.data.status === "pending") return Timer;
  if (props.data.status === "submitted") return Finished;
  if (props.data.status === "returned") return Checked;
});

const statusColor = computed(() => {
  if (props.data.status === "pending") return "red";
  if (props.data.status === "submitted") return "orange";
  if (props.data.status === "returned") return "green";
});

const scoreColor = computed(() => {
  if (props.data.status !== "returned") return "#666"; // 默认灰色
  const ratio = props.data.score / props.data.max_score;
  const red = Math.round(255 * (1 - ratio));
  const green = Math.round(255 * ratio);
  return `rgb(${red}, ${green}, 0)`;
});

const statusText = computed(() => {
  if (props.data.status === "pending") return "未提交";
  if (props.data.status === "submitted") return "已提交";
  if (props.data.status === "returned") return "已公布分数";
});

const displayScore = computed(() => (props.data.status === "returned" ? props.data.score : "--"));
const displayTotalScore = computed(() => (props.data.status === "returned" ? props.data.max_score : "--"));

const isEditing = ref(false);
const editingText = ref('');
const editingFileList = ref([]);

const editSubmittedAssignment = (content, editing_code, attachments) => {
  editingText.value = JSON.parse(JSON.stringify(content));
  editingFileList.value = JSON.parse(JSON.stringify(attachments));
  code.value = "123";
  selectedLanguage.value = JSON.parse(JSON.stringify(editing_code.language));
  updateMode();
  isEditing.value = true;
}

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

.submit-btn {
  margin-left: auto;
  margin-right: 20px;
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
}

.submit-btn:hover {
  background-color: #66b1ff;
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
</style>
