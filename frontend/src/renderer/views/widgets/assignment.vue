<template>
  <widget-card :title="computedTitle" type="assignment" :button-visible="editable" @click="handleClick">
    <div class="container" v-if="isEditingHomework">
      <!--   编辑作业信息   -->
      <div>
        <el-text class="section-title">作业设置</el-text>
        <div class="homework-form">
          <el-form :model="form" :rules="rules" label-width="120px">
            <!-- 作业标题 -->
            <el-form-item label="作业标题" prop="title">
              <el-input v-model="form.title" placeholder="请输入作业标题"></el-input>
            </el-form-item>

            <!-- 作业类型 -->
            <el-form-item label="作业类型" prop="type">
              <el-select v-model="form.submitType" placeholder="请选择作业类型">
                <el-option v-for="item in AssignmentType" :label="item.label" :value="item.value"/>
              </el-select>
            </el-form-item>

            <!-- 作业截止时间 -->
            <el-form-item label="作业截止时间" prop="ddl">
              <el-date-picker
                  v-model="form.ddl"
                  type="datetime"
                  placeholder="选择截止时间"
                  format="YYYY-MM-DD HH:mm:ss"
                  value-format="YYYY-MM-DD HH:mm:ss"
              ></el-date-picker>
            </el-form-item>

            <!-- 作业分数上限 -->
            <el-form-item label="分数上限" prop="maxScore">
              <el-input-number v-model="form.maxScore" :min="0" :max="100"
                               placeholder="请输入分数上限"></el-input-number>
            </el-form-item>

            <!-- 作业是否可见 -->
            <el-form-item label="是否可见" prop="isVisible">
              <el-switch v-model="form.visible" active-text="是" inactive-text="否"></el-switch>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <!--   作业信息   -->
      <div>
        <el-text class="section-title">作业信息</el-text>
        <el-text> 注意：这里提交的是作业的附加文件，不是测试用例哦！</el-text>
        <md-and-file-editor
            ref="homeworkContentEditor"
            :fileList="form.attachments"
            :content="form.content"
            @upload="handleHomeworkContentEditorUpdate"
            @remove="handleHomeworkContentEditorRemove"
        />
      </div>
      <!--   测试设置   -->
      <div v-if="form.submitType === 'code'">
        <el-text class="section-title">测试用例</el-text>
        <el-form :model="testcaseForm" label-width="100px">
          <el-form-item label="时间限制">
            <el-input-number
                v-model="testcaseForm.maxCpuTime"
                :min="1"
                :max="10000"
                :step="1000"
                controls-position="right"
            >
              <template #suffix>ms</template>
            </el-input-number>
          </el-form-item>

          <el-form-item label="空间限制">
            <el-input-number
                v-model="testcaseForm.maxMemory"
                :min="1"
                :max="2048"
                :step="128"
                controls-position="right"
            >
              <template #suffix>MB</template>
            </el-input-number>
          </el-form-item>

          <el-form-item label="测试数据">
            <el-upload
                :show-file-list="false"
                :http-request="handleUploadTestcaseZipFile"
            >
              <el-button type="primary">上传文件</el-button>
            </el-upload>
            <el-text style="margin-left: 10px" v-show="testcaseZipFileName.length !== 0">
              已上传文件名：{{testcaseZipFileName}}
            </el-text>
          </el-form-item>
        </el-form>

        <el-button @click="handleUploadTestcase">
          上传测试用例
        </el-button>
      </div>

      <div v-if="form.submitType === 'code'">
        <el-text class="section-title">测试点信息</el-text>
        <el-table :data="formattedTestcaseInfo" border style="width: 100%" v-if="formattedTestcaseInfo.length !== 0">
          <el-table-column prop="key" label="测试点编号" width="120" />
          <el-table-column prop="inputName" label="输入文件名" />
          <el-table-column prop="inputSizeFormatted" label="输入文件大小" />
          <el-table-column prop="outputName" label="输出文件名" />
          <el-table-column prop="outputSizeFormatted" label="输出文件大小" />
        </el-table>
        <el-text v-else>
          当前还没上传过测试点！
        </el-text>
      </div>
    </div>

    <div class="container" v-else>
      <!--   作业状态   -->
      <div>
        <el-text class="section-title">作业状态</el-text>
        <div class="assignment-status">
          <el-row class="status-row">
            <!-- 状态信息 -->
            <el-col :span="12" class="status-text">
              <el-icon :size="28" class="status-icon" :color="statusColor">
                <component :is="statusIcon"/>
              </el-icon>
              <el-text>
                {{ statusText + "，提交截止时间：" + timestampToString(props.data.ddl)}}
              </el-text>
            </el-col>

            <!-- 得分展示 -->
            <el-col :span="12" class="score-display">
              <span class="score" :style="{ color: scoreColor }">{{ displayScore }}</span>
              <span class="total-score"> / {{ props.data.maxScore }}</span>
            </el-col>
          </el-row>
        </div>
      </div>

      <!--   作业信息   -->
      <div>
        <el-text class="section-title">作业信息</el-text>
        <el-descriptions :column="2" size="small" border v-if="props.data.submitType === 'code'">
          <el-descriptions-item label="时间限制">
            {{ props.data.testCase?.maxCpuTime ?? '--' }} ms
          </el-descriptions-item>
          <el-descriptions-item label="空间限制">
            {{ formatSize(props.data.testCase?.maxMemory ?? 0) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <div>
        <md-and-file :fileList="props.data.attachments" :content="props.data.content"/>
      </div>

      <!--   批改建议   -->
      <div v-if="props.data.feedback">
        <el-text class="section-title">批改建议</el-text>
        <div class="container">
          <md-and-file :file-list="props.data.feedback?.attachments" :content="props.data.feedback?.content"/>
          <el-button
              type="primary"
              :icon="ChatRound"
              :disabled="props.data.submitType === 'code'"
              @click="postArgue"
              style="width: 140px; margin-right: auto"
          >
            我要 Argue ！
          </el-button>
        </div>
      </div>

      <!--   提交记录   -->
      <div>
        <el-text tag="h4" class="section-title">提交记录</el-text>
        <el-row
            class="submit-record-item"
            justify="space-between"
        >
          <el-col :span="1">
            <el-icon :size="20">
              <component :is="EditPen"/>
            </el-icon>
          </el-col>
          <el-col :span="8">
            <el-text truncated>开始新的提交</el-text>
          </el-col>
          <el-col :span="8"/>
          <el-col :span="6" class="edit-button">
            <el-button
                type="primary"
                link
                :icon="Edit"
                @click="beginNewSubmission"
            >
              开始
            </el-button>
          </el-col>
        </el-row>
        <el-row
            v-for="record in props.data.submittedAssignment"
            :key="record.submittedTime"
            class="submit-record-item"
            justify="space-between"
        >
          <el-col :span="1">
            <el-icon :size="20">
              <component :is="Memo"/>
            </el-icon>
          </el-col>
          <el-col :span="8">
            <el-text truncated>提交时间：{{ timestampToString(record.submittedTime) }}</el-text>
          </el-col>
          <el-col :span="8">
            <el-text truncated>批改状态：{{ record.feedback ? '得分：' + record.feedback.score : '未批改' }}</el-text>
          </el-col>
          <el-col :span="6" class="edit-button">
            <el-button
                type="primary"
                link
                :icon="Edit"
                @click="editSubmittedAssignment(record)"
            >
              查看
            </el-button>
          </el-col>
        </el-row>
      </div>

      <!--    本次提交批改建议    -->
      <div v-if="currentFeedback !== null">
        <el-text class="section-title">本次提交批改建议</el-text>
        <div class="container">
          <md-and-file :file-list="currentFeedback.attachments" :content="currentFeedback.content"/>
        </div>
      </div>

      <!--   提交作业区   -->
      <div v-if="isEditing">
        <el-text class="section-title">提交作业</el-text>
        <div class="container">
          <!--   提交代码   -->
          <div class="code-editor" v-if="props.data.submitType === 'code'">
            <div class="toolbar">
              <span class="el-text">选择语言：</span>
              <el-select v-model="selectedLanguage" size="small" @change="updateMode">
                <el-option v-for="lang in languages" :key="lang.value" :label="lang.label" :value="lang.value"/>
              </el-select>
            </div>
            <div style="width: 100%; height: 100%;">
              <code-editor ref="codeEditor" :language="selectedLanguage" :code="code"/>
            </div>
          </div>
          <!--   提交文本或文件   -->
          <div class="homework-editor" v-if="props.data.submitType === 'file'">
            <md-and-file-editor
                :content="content"
                :fileList="fileList"
                ref="contentEditor"
                @upload="handleSubmissionAttachmentUpload"
                @remove="handleSubmissionAttachmentRemove"
            />
          </div>
          <el-button
              type="primary"
              :icon="Upload"
              @click="submit"
              style="width: 120px; margin-left: auto"
          >
            提交作业
          </el-button>
        </div>
      </div>
    </div>

    <template #button>
      <template v-if="isEditingHomework">
        <el-icon>
          <Check/>
        </el-icon>
        <span>保存</span>
      </template>
      <template v-else>
        <el-icon>
          <Edit/>
        </el-icon>
        <span>编辑</span>
      </template>
    </template>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "./utils/widget-card.vue";
import MdAndFile from "./utils/md-and-file.vue";
import MdAndFileEditor from "./utils/md-and-file-editor.vue";
import CodeEditor from "./utils/code-editor.vue";
import {computed, onMounted, ref} from "vue";
import {ChatRound, Checked, Edit, Finished, Memo, Timer, Upload, Check, EditPen} from "@element-plus/icons-vue";
import type {AssignmentWidget, Feedback, SubmittedRecord, Testcase} from "@/types/widgets";
import {FileMeta} from "@/types/fileMeta";
import {
  addWidgetAttachment,
  removeWidgetAttachment,
  createSubmission,
  createSubmissionAttachment,
  editAssignmentWidget,
  Submission,
  getTestcase, createTestcase, editTestcase, createAssignmentWidget
} from "@/api/courseMaterial";
import {ElMessage} from "element-plus";
import {WidgetUnion} from "@/types/widgets";
import {useUploader} from "@/composables/useUploader";
import router from "../../router";

/*
* 数据和常量
* */

const props = defineProps<{
  pageId: number;
  data: AssignmentWidget;
  editable: boolean;
}>();

onMounted(async () => {
  if (props.data.id === 0) await handleClick();
})

const AssignmentType = [
  {label: "文本及附件", value: "file"},
  {label: "评测代码", value: "code"},
]

/*
* 外观
* */

/*
* 代码编辑器的所有常量和方法：
* languages：可选的语言（label），以及monaco切换高亮模式需要的名字（value）
* selectedLanguage：已选的语言（value）
* code：代码编辑器的内容
* updateMode：当已选语言改变时触发，但目前使用了ref所以不需要执行任何东西（不需要通知monaco）
* */
const languages = [
  {label: "C++", value: "cpp", backend: "cpp"},
  {label: "C", value: "c", backend: "c"},
  {label: "Java", value: "java", backend: "java"},
  {label: "Python", value: "python", backend: "py3"},
];
const updateMode = () => {
  // Nothing
};

const codeEditor = ref<InstanceType<typeof CodeEditor> | null>(null);
const contentEditor = ref<InstanceType<typeof MdAndFileEditor> | null>(null);  // 提交文本作业时用的编辑器
const homeworkContentEditor = ref<InstanceType<typeof MdAndFileEditor> | null>(null);  // 编辑作业信息时用的编辑器

// 本卡片的标题
const computedTitle = computed(() => props.data?.title || "作业");

// 状态区的所有方法，都是外观特效
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
  if (props.data.status !== "returned") return "#666";
  const ratio = props.data.score / props.data.maxScore;
  const red = Math.round(255 * (1 - ratio));
  const green = Math.round(255 * ratio);
  return `rgb(${red}, ${green}, 0)`;
});
const timestampToString = (timestamp: string) => {
  if (timestamp.length === 0) return '';
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(timestamp));
};
const statusText = computed(() => {
  if (props.data.status === "pending") return "未提交";
  if (props.data.status === "submitted") return "已提交";
  if (props.data.status === "returned") return "已公布分数";
});
const displayScore = computed(() => (props.data.status === "returned" ? props.data.score : "--"));

/*
* 编辑作业信息
* */

const isEditingHomework = ref(false);
const form = ref<AssignmentWidget>({});
const rules = {
  title: [{required: true, message: '请输入作业标题', trigger: 'blur'}],
  type: [{required: true, message: '请选择作业类型', trigger: 'change'}],
  ddl: [{required: true, message: '请选择作业截止时间', trigger: 'change'}],
  maxScore: [{required: true, message: '请输入分数上限', trigger: 'blur'}],
};

const emit = defineEmits<{
  (e: "update", data: WidgetUnion): void;
}>();

const handleHomeworkContentEditorUpdate = async (file: FileMeta) => {
  const index = form.value.attachments.findIndex(f => f.id === file.id);
  if (index === -1) {
    form.value.attachments.push(file);
  }
}

const handleHomeworkContentEditorRemove = async (file: FileMeta) => {
  const index = form.value.attachments.findIndex(f => f.id === file.id);
  if (index !== -1) {
    form.value.attachments.splice(index, 1);
  }
}

const testcaseForm = ref<Testcase>({})
const testcaseInfo = ref({})
const testcaseZipFileName = ref('')

function formatSize(bytes: number): string {
  if (bytes === 0) return '--'
  if (bytes >= 1048576) return (bytes / 1048576).toFixed(2) + ' MB'
  if (bytes >= 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return bytes + ' B'
}

const formattedTestcaseInfo = computed(() =>
    Object.entries(testcaseInfo.value)
        .sort(([a], [b]) => parseInt(a) - parseInt(b))
        .map(([key, value]) => ({
          key,
          inputName: value.inputName,
          inputSizeFormatted: formatSize(value.inputSize),
          outputName: value.outputName,
          outputSizeFormatted: formatSize(value.outputSize)
        }))
)

const handleClick = async () => {
  if (isEditingHomework.value) {  // 点保存：上传至后端
    form.value.content = homeworkContentEditor.value?.getContent()
    if (!(form.value.ddl?.length ?? 0)) {
      ElMessage.error("请选择截止时间")
      return
    }
    let message = "";

    const oldAttachments = props.data.attachments || [];
    const newAttachments = form.value.attachments || [];

    const addedFiles = newAttachments.filter(f => !oldAttachments.some(o => o.id === f.id));
    const removedFiles = oldAttachments.filter(f => !newAttachments.some(n => n.id === f.id));

    const editResponse = props.data.id === 0 ?
        await createAssignmentWidget(form.value as AssignmentWidget, props.pageId):
        await editAssignmentWidget(form.value as AssignmentWidget);
    if (editResponse.status !== 200) {
      message += "保存文本失败\n";
    }

    for (const file of addedFiles) {
      const res = await addWidgetAttachment(props.data.id, file.id);
      if (res.status !== 200) message += `附件添加失败：${file.name}\n`;
    }

    for (const file of removedFiles) {
      const res = await removeWidgetAttachment(file.id);
      if (res.status !== 200) message += `附件删除失败：${file.name}\n`;
    }

    if (message !== "") {
      ElMessage.error(message);
    } else {
      ElMessage.success("保存成功");
      console.log(editResponse.data);
      emit("update", editResponse.data);
    }

  } else {  // 点编辑：将现有信息填入表单
    // 题目信息
    form.value = JSON.parse(JSON.stringify(props.data));
    // 测试信息
    if (props.data.testCase?.id) {
      testcaseForm.value = props.data.testCase;
      testcaseForm.value.maxMemory /= 1048576;
      const response = await getTestcase(props.data.id);
      if (response.status === 200) {
        testcaseInfo.value = response.data.info.testCases;
      } else {
        console.log(response)
      }
    } else {
      testcaseForm.value = {
        id: 0,
        widgetId: props.data.id,
        maxCpuTime: 1000,
        maxMemory: 128,
        fileId: '',
      }
      testcaseInfo.value = {};
    }

  }
  isEditingHomework.value = !isEditingHomework.value;
}

const {upload} = useUploader();

const handleUploadTestcaseZipFile = async (options: any) => {
  const {file, onSuccess, onError} = options;

  try {
    const response = await upload(file);
    if (response.status === 200) {
      ElMessage.success("上传成功");
      testcaseForm.value.fileId = (response.data as FileMeta).id;
      testcaseZipFileName.value = (response.data as FileMeta).filename;
      onSuccess(response.data);
    } else {
      ElMessage.error("上传失败，请稍后再试");
      onError(response)
    }
  } catch (err) {
    ElMessage.error("上传失败，未知错误");
    onError(err);
  }
};

const handleUploadTestcase = async () => {
  const response = testcaseForm.value.id === 0 ?
          await createTestcase(testcaseForm.value):
          await editTestcase(testcaseForm.value);
  if (response.status === 200) {
    ElMessage.success("更新测试数据成功！")
    testcaseInfo.value = response.data.info?.testCases ?? testcaseInfo.value ?? {};
  } else {
    ElMessage.error("更新测试数据失败！")
  }
}

/*
 * 提交作业
 */

const isEditing = ref(false);
const currentFeedback = ref<Feedback | null>(null);
const selectedLanguage = ref<string>("cpp");
const code = ref<string>('');
const content = ref<string>("");
const fileList = ref<FileMeta[]>([]);

const beginNewSubmission = () => {
  code.value = '';
  selectedLanguage.value = 'cpp';
  content.value = '';
  contentEditor.value?.updateContent(content.value);
  fileList.value = [];
  currentFeedback.value = null;
  isEditing.value = true;
}

const editSubmittedAssignment = (record: SubmittedRecord) => {
  if (props.data.submitType === 'code') {
    code.value = JSON.parse(JSON.stringify(record.code?.code ?? ''));
    selectedLanguage.value = JSON.parse(JSON.stringify(record.code?.language ?? 'cpp'));
    selectedLanguage.value = languages.find(l => l.backend === selectedLanguage.value)?.value;
    currentFeedback.value = record.feedback;
  } else if (props.data.submitType === 'file') {
    content.value = JSON.parse(JSON.stringify(record.content ?? ''));
    contentEditor.value?.updateContent(content.value);
    fileList.value = JSON.parse(JSON.stringify(record.attachments ?? []));
  } else {
    ElMessage.error("加载提交记录失败：未知作业类型")
  }
  currentFeedback.value = record.feedback;
  isEditing.value = true;
}

const handleSubmissionAttachmentUpload = async (file: FileMeta) => {
  const index = fileList.value.findIndex(f => f.id === file.id);
  if (index === -1) {
    fileList.value.push(file);
  }
}

const handleSubmissionAttachmentRemove = async (file: FileMeta) => {
  const index = fileList.value.findIndex(f => f.id === file.id);
  if (index !== -1) {
    fileList.value.splice(index, 1);
  }
}

const submit = async () => {
  let submission: Submission = {
    widgetId: props.data.id
  };
  let submissionAttachments: FileMeta[] = [];
  if (props.data.submitType === 'code') {
    if (codeEditor.value) {
      submission.code = {
        code: codeEditor.value.getCode(),
        language: languages.find(l => l.value === selectedLanguage.value)?.backend,
      }
    } else {
      ElMessage.error("提交失败：未找到代码编辑框")
    }
  } else if (props.data.submitType === 'file') {
    if (contentEditor.value) {
      submission.content = contentEditor.value.getContent();
      submissionAttachments = fileList.value;
    } else {
      ElMessage.error("提交失败：未找到文本编辑框")
    }
  } else {
    ElMessage.error("提交失败：未知作业类型")
  }
  const response = await createSubmission(submission)
  if (response.status === 200) {
    let failed = false;
    for (const attachment of submissionAttachments) {
      const response2 = await createSubmissionAttachment(response.data.id, attachment.id);
      if (response2.status !== 200) {
        ElMessage.error("提交失败：附件 " + attachment.filename + " 上传失败");
        failed = true;
        break;
      }
    }
    if (!failed) {
      ElMessage.success("提交成功！");
      window.location.reload();
    }
  } else {
    ElMessage.error("提交失败：未能创建提交，请稍后再试");
  }
}

// 发起 argue
const postArgue = () => {
  if ('argue_id' in props.data && Number.isInteger(props.data.argue_id)) {
    // 路由到对应的Argue的页面
    router.push({path: `/argue/${props.data.argue_id}`});
  } else {
    // 路由到创建Argue的页面
    router.push({
      path: `/argue/new`,
      query: {
        widgetId: props.data.id,
      }
    });
  }
}


defineExpose({
  init: () => {
    codeEditor.value?.layout()
  }
});
</script>

<style scoped>
.container {
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

.section-title {
  display: block;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #303133;
}

.section-title {
  position: relative;
  padding-left: 24px;
}

.section-title::before {
  content: '>';
  position: absolute;
  left: 0;
  top: 0;
  color: #409EFF;
  font-weight: bold;
  font-size: 22px;
  transform: translateY(1px);
}
</style>
