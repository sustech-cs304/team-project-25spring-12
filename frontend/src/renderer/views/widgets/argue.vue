<template>
  <widget-card :title="computedTitle" color="orange" icon="Opportunity">
    <div class="overall_container">
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
          <div class="homework-editor" v-if="props.data.submitType === 'file'">
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
        </el-row>
        <div class="container">
          <md-and-file :fileList="props.data.submittedArguement.attachments" :content="props.data.submittedArguement.content"/>
        </div>
      </div>

      <!-- 投票结果 -->
      <div v-if="props.data.status !== 'pending'">
        <el-text class="section-title">讨论区</el-text>
        <el-row>
          <el-table :data="tableVote">
            <el-table-column label="投票结果">
              <el-progress
                :percentage=votePercentage
                color="#49CD62"
                :stroke-width="20"
                :show-text=true
                :status=voteStatus
                :indeterminate=voteIndeterminate
              >
              <el-text type="primary">{{ props.data.voteSupport }} / {{ props.data.voteTotal }}</el-text>
              </el-progress>
            </el-table-column>
            <el-table-column label="投票" width="200">
              <div style="display: flex; align-items: center">
                <!-- <el-button-group> -->
                  <el-button onclick="vote(true)" type="success">支持</el-button>
                  <el-button onclick="vote(false)" type="warning">反对</el-button>
                <!-- </el-button-group> -->
              </div>
            </el-table-column>
          </el-table>
        </el-row>
        <div class="comment-section">
          <!-- 发布新评论 -->
          <div class="comment-input">
            <el-input
              v-model="newComment"
              type="textarea"
              :rows="3"
              placeholder="请输入您的评论..."
              resize="none"
            ></el-input>
            <div class="input-actions">
              <el-button type="primary" @click="submitComment" :disabled="!newComment.trim()">发布评论</el-button>
            </div>
          </div>

          <!-- 评论列表 -->
          <div class="comment-list">
            <div
              v-for="comment in comments"
              :key="comment.id"
              class="comment-item"
            >
              <div class="comment-header">
                <span class="author">{{ comment.author }}</span>
                <span class="time">{{ comment.time }}</span>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
              <div class="comment-actions">
                <el-button type="text" @click="handleReply(comment.author)">回复</el-button>
              </div>
            </div>
          </div>
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

const votePercentage = computed(() => {
  return props.data.voteTotal === 0 ?
    0 : Math.round(props.data.voteSupport / props.data.voteTotal * 100);
})
const voteStatus = computed(() => {
  return props.data.voteTotal === 0 ? "warning" : null;
});
const voteIndeterminate = computed(() => {
  return props.data.voteTotal === 0 ? true : false;
});

interface VoteResult {
  percentage: number
  status: string
  indeterminate: boolean
}
const tableVote: VoteResult[] = [
  {
    percentage: props.data.voteTotal === 0 ?
      0 : Math.round(props.data.voteSupport / props.data.voteTotal * 100),
    status: props.data.voteTotal === 0 ? "warning" : "",
    indeterminate: props.data.voteTotal === 0 ? true : false,
  },
]

const submitArgue = () => {
  const content = contentEditor.value?.getContent();
}

const editArgue = () =>{

}

const reviseArgue = () => {

}

const vote = (isSupport) => {
  
}

// 评论数据
const comments = ref([
  {
    id: 1,
    content: '这是一条示例评论！',
    author: '用户1',
    time: '2025-06-04 16:00'
  }
]);

// 新评论内容
const newComment = ref('');

// 发布新评论
const submitComment = () => {
  if (!newComment.value.trim()) return;
  
  const comment = {
    id: Date.now(),
    content: newComment.value,
    author: '当前用户',
    time: new Date().toLocaleString()
  };
  
  comments.value.unshift(comment);
  newComment.value = '';
};

// 处理回复
const handleReply = (author) => {
  newComment.value = `@${author} `;
};
</script>


<style scoped>
.overall_container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
  background-color: transparent;
  border-radius: 12px;
  max-width: 1200px;
  margin: 0 auto;
}
.container {
  display: flex;
  flex-direction: column;
  padding: 0;
  background-color: transparent;
  border: none;
  gap: 20px;
  /* padding: 20px; */
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

/* .el-text {
  margin-right: 8px;
  font-size: 14px;
  color: #606266;
} */

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
  /* background: #409eff; */
  /* color: #fff; */
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

.comment-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.comment-input {
  margin-bottom: 20px;
}

.comment-input .el-textarea {
  margin-bottom: 10px;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 15px;
  background: #fff;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.author {
  font-weight: bold;
}

.time {
  color: #909399;
  font-size: 12px;
}

.comment-content {
  margin-bottom: 10px;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}
</style>
  