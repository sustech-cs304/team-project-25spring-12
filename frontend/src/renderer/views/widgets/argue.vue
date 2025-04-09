<template>
  <widget-card :title="computedTitle" color="orange" icon="Opportunity">
    <div class="container">
      <!-- 辩驳状态 -->
      <div>
        <el-text class="section-title">辩驳状态</el-text>
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
                <span class="original-score" :style="{ color: originalScoreColor }">{{ displayOriginalScore }}</span>
                / 
                <span class="verified-score" :style="{ color: verifiedScoreColor }">{{ displayVerifiedScore }}</span>
                / 
                <span class="max-score">{{ displayMaxScore }}</span>
              </el-col>
            </el-row>
          </div>
      </div>
    </div>

    <!-- 作业信息 -->
    <div>
      <el-text class="section-title">作业信息</el-text>
      <md-and-file :fileList="props.data.attachments" :content="props.data.content"/>
    </div>
    
    <!-- 批改建议 -->
    <div>
      <el-text class="section-title">批改建议</el-text>
      <div class="container">
        <md-and-file :fileList="props.data.returnedFiles" :content="props.data.feedback"/>
      </div>
    </div>

    <!-- 辩驳反馈 -->
    <div v-if="props.data.status === 'returned'">
      <el-text class="section-title">辩驳反馈</el-text>
      <div class="container">
        <md-and-file :fileList="props.data.argueReturnedFiles" :content="props.data.argueFeedback"/>
      </div>
    </div>

    <!-- 提交争辩区 -->
    <div class="argue-submit" v-if="props.data.status === 'pending' || isEditing">
      <el-text class="section-title">辩驳理由</el-text>
      <div class="container">
        <div class="homework-editor" v-if="props.data.submitTypes.includes('file')">
          <md-and-file-editor :content="content" :fileList="fileList" ref="contentEditor"/>
        </div>
        <el-button
            type="primary"
            :icon="Upload"
            @click="submit"
            style="width: 120px; margin-left: auto"
        >
          提交辩驳
        </el-button>
      </div>
    </div>
    
    <!-- 辩驳记录 -->
    <!-- 设定只能Argue一次 -->
    <div v-if="props.data.status !== 'pending'">
      <el-text class="section-title">辩驳记录</el-text>
      <el-row>
        <el-col :span="1">
          <el-icon :size="20">
            <component :is="Memo"/>
          </el-icon>
        </el-col>
        <el-col :span="16">
          <el-text truncated>提交时间：{{ props.data.submittedArguement.time }}</el-text>
        </el-col>
        <!-- <el-col :span="6" class="edit-button">
          <el-button
              type="primary"
              link
              :icon="Edit"
              @click="editSubmittedArguement(props.data.submittedArguement)"
          >
            编辑
          </el-button>
        </el-col> -->
      </el-row>
      <div class="container">
        <md-and-file :fileList="props.data.submittedArguement.attachments" :content="props.data.submittedArguement.content"/>
      </div>
    </div>
  </widget-card>
</template>
  
<script setup lang="ts">
  import WidgetCard from "./utils/widget-card.vue";
  import MdAndFile from "./utils/md-and-file.vue";
  import MdAndFileEditor from "./utils/md-and-file-editor.vue";
  import {computed, ref} from "vue";
  import {Checked, Edit, Finished, Memo, Timer, Upload, ChatRound} from "@element-plus/icons-vue";
  
  const props = defineProps({
    data: {
      type: Object,
      required: true,
    },
  });
  
  const contentEditor = ref<InstanceType<typeof MdAndFileEditor> | null>(null);
  
  // 本卡片的标题
  const computedTitle = computed(() => props.data?.title || "辩驳");
  
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
  const originalScoreColor = computed(() => {
    if (props.data.status === "returned") return "#999";
    const ratio = props.data.originalScore / props.data.maxScore;
    const red = Math.round(255 * (1 - ratio));
    const green = Math.round(255 * ratio);
    return `rgb(${red}, ${green}, 0)`;
  });
  const verifiedScoreColor = computed(() => {
    if (props.data.status === "pending") return "#666";
    const ratio = props.data.verifiedScore / props.data.maxScore;
    const red = Math.round(255 * (1 - ratio));
    const green = Math.round(255 * ratio);
    return `rgb(${red}, ${green}, 0)`;
  });
  const statusText = computed(() => {
    if (props.data.status === "pending") return "未提交";
    if (props.data.status === "submitted") return "已提交";
    if (props.data.status === "returned") return "已反馈";
  });
  const displayOriginalScore = props.data.originalScore;
  const displayVerifiedScore = computed(() => (props.data.status === "returned" ? props.data.verifiedScore : "--"));
  const displayMaxScore = props.data.maxScore;
  
  // 编辑提交记录
  const isEditing = ref(false);  // if (pending || isEditing) then /*展示提交作业区域*/
  const content = ref("");
  const fileList = ref([]);
  const editSubmittedArguement = (record: any) => {
    content.value = JSON.parse(JSON.stringify(record.content));
    fileList.value = JSON.parse(JSON.stringify(record.attachments));
    // updateMode();
    isEditing.value = true;
  }
  
  // 提交辩驳
  const submit = () => {
  // TODO
    if (contentEditor.value) {
      const content = contentEditor.value.getContent();
      console.log(content);
      const fileList = contentEditor.value.getFileList();
      console.log(fileList);
    }
  }
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
  
  .original-score {
    font-size: 22px;
    font-weight: 700;
  }

  .verified-score {
    font-size: 24px;
    font-weight: 700;
  }
  
  .max-score {
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
  