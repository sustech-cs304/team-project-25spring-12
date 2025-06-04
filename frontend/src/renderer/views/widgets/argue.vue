<template>
  <widget-card :title="computedTitle" color="orange" icon="Opportunity">
    <div class="overall_container">
      <!-- 工具栏：关注按钮和打分框 -->
      <div class="toolbar">
        <!-- 关注按钮 -->
        <div class="follow-section">
          <el-button
            :type="isFollowed ? 'primary' : 'default'"
            @click="toggleFollow"
            :icon="isFollowed ? 'StarFilled' : 'Star'"
          >
            {{ isFollowed ? '已关注' : '关注' }} ({{ followCount }})
          </el-button>
        </div>
        <!-- 打分框（仅教师可见） -->
        <div class="score-section" v-if="isTeacher">
          <el-input-number
            v-model="revisedScore"
            :min="0"
            :max="props.data.maxScore"
            placeholder="输入评分"
            size="small"
            style="width: 120px; margin-right: 10px;"
          />
          <el-button
            type="primary"
            @click="submitArgueFeedback"
            :disabled="revisedScore === null"
          >
            提交评分
          </el-button>
        </div>
      </div>

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
                <span class="Revised-score" :style="{ color: revisedScoreColor }">{{ displayRevisedScore }}</span>
                / 
                <span class="max-score">{{ displayMaxScore }}</span>
              </el-col>
            </el-row>
          </div>
      </div>

      <!-- 作业信息 -->
      <div>
        <el-text class="section-title">作业信息</el-text>
        <md-and-file
          :fileList="props.data.assignmentFileList"
          :content="props.data.assignmentContent"
        />
      </div>
    
      <!-- 批改建议 -->
      <div>
        <el-text class="section-title">批改建议</el-text>
        <div class="container">
          <md-and-file
            :fileList="props.data.feedbackFileList"
            :content="props.data.feedbackContent"
          />
        </div>
      </div>

      <!-- 提交争辩区 -->
      <div v-if="isEditing">
        <el-text class="section-title">提交辩驳</el-text>
        <div class="container">
          <!--   提交文本或文件   -->
          <div class="homework-editor">
            <md-and-file-editor
                :content="argueContent"
                :fileList="argueFileList"
                ref="contentEditor"
                @upload="handleArgueAttachmentUpload"
                @remove="handleArgueAttachmentRemove"
            />
          </div>
          <el-button
              type="primary"
              :icon="Upload"
              @click="submitArgue"
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
            <el-text truncated>
              提交时间：{{ props.data.submittedArguement.updateTime }}
            </el-text>
          </el-col>
        </el-row>
        <div class="container">
          <md-and-file
            :fileList="argueFileList"
            :content="argueContent"
          />
        </div>
      </div>

      <!-- 教师编辑辩驳反馈 -->
      <div v-if="isTeacher">
        <el-text class="section-title">编辑辩驳反馈</el-text>
        <div class="container">
          <md-and-file-editor
            :fileList="props.data.argueFeedbackFilelist"
            :content="props.data.argueFeedbackContent"
            ref="contentEditor"
            @upload="handleArgueFeedbackAttachmentUpload"
            @remove="handleArgueFeedbackAttachmentRemove"
          />
        </div>
      </div>

      <!-- 辩驳反馈 -->
      <div v-if="props.data.status === 'returned' && !isTeacher">
        <el-text class="section-title">辩驳反馈</el-text>
        <div class="container">
          <md-and-file
            :fileList="props.data.argueFeedbackFilelist"
            :content="props.data.argueFeedbackContent"
          />
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
              <el-text type="primary">{{ voteSupport }} / {{ voteTotal }}</el-text>
              </el-progress>
            </el-table-column>
            <el-table-column label="投票" width="200">
              <div style="display: flex; align-items: center">
                <!-- <el-button-group> -->
                  <el-button
                    :disabled="hasVoted"
                    @click="vote(true)"
                    type="success"
                  >
                    支持
                  </el-button>
                  <el-button
                    :disabled="hasVoted"
                    @click="vote(false)"
                    type="warning"
                  >
                    反对
                  </el-button>
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
import {computed, onMounted, ref} from "vue";
import {Checked, Edit, Finished, Memo, Timer, Upload, ChatRound} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import {useUploader} from "@/composables/useUploader";
import {getRoleByCourseId} from "@/composables/useUserData";
import router from "../../router";
import { FileMeta } from "../../types/fileMeta";
import service from "../../utils/request";
import { Feedback } from "../../types/widgets";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const argueEditor = ref<InstanceType<typeof MdAndFileEditor> | null>(null);
const argueFeedbackEditor = ref<InstanceType<typeof MdAndFileEditor> | null>(null);

const argueId = ref(-1);

// 关注状态和人数
const isFollowed = ref(false);
const followCount = ref(0); // 假设初始关注人数为0

// 教师评分
const isTeacher = ref(true); // 假设当前用户是教师，实际应从用户角色权限中获取
const revisedScore = ref<number | null>(null);

// 切换关注状态
const toggleFollow = () => {
  try {
    if (isFollowed.value) {
      service.post('/argue/watch', {
        arguePostId: props.data.id,
      });
  } else {
    service.delete(`/argue/${argueId}/watch`);
  }
    isFollowed.value = !isFollowed.value;
    followCount.value += isFollowed.value ? 1 : -1;
    ElMessage.success(isFollowed.value ? "已关注" : "已取消关注");
  } catch (error) {
    ElMessage.error("操作失败，请稍后再试");
  }
};

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
const revisedScoreColor = computed(() => {
  if (props.data.status === "pending") return "#666";
  const ratio = props.data.revisedScore / props.data.maxScore;
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
const displayRevisedScore = computed(() =>
  (props.data.status === "returned" ? props.data.revisedScore : "--")
);
const displayMaxScore = props.data.maxScore;

// 提交作业区
const isEditing = ref(false);
const argueContent = ref("");
const argueFileList = ref<FileMeta[]>([]);
const argueFeedbackContent = ref("");
const argueFeedbackFileList = ref<FileMeta[]>([]);

const handleArgueAttachmentUpload = async (file: FileMeta) => {
  const index = argueFileList.value.findIndex(f => f.id === file.id);
  if (index === -1) {
    argueFileList.value.push(file);
  }
}

const handleArgueAttachmentRemove = async (file: FileMeta) => {
  const index = argueFileList.value.findIndex(f => f.id === file.id);
  if (index !== -1) {
    argueFileList.value.splice(index, 1);
  }
}

const handleArgueFeedbackAttachmentUpload = async (file: FileMeta) => {
  const index = argueFeedbackFileList.value.findIndex(f => f.id === file.id);
  if (index === -1) {
    argueFileList.value.push(file);
  }
}

const handleArgueFeedbackAttachmentRemove = async (file: FileMeta) => {
  const index = argueFeedbackFileList.value.findIndex(f => f.id === file.id);
  if (index !== -1) {
    argueFileList.value.splice(index, 1);
  }
}

// 投票区
const voteSupport = ref(props.data.voteSupport)
const voteTotal = ref(props.data.voteTotal)
const hasVoted = ref(false)

const votePercentage = computed(() => {
  return voteTotal.value === 0 ?
    0 : Math.round(voteSupport.value / voteTotal.value * 100);
})
const voteStatus = computed(() => {
  return voteTotal.value === 0 ? "warning" : null;
});
const voteIndeterminate = computed(() => {
  return voteTotal.value === 0 ? true : false;
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

const vote = async (isSupport: boolean) => {
  // try {
  //   模拟发送投票请求到后端
  //   const response = await service.post('/argue/vote', {
  //     isSupport: isSupport,
  //   })

  //   if (response.data.success) {
  //     更新前端数据
      voteTotal.value += 1
      if (isSupport) {
        voteSupport.value += 1
      }
      hasVoted.value = true // 锁定投票
      ElMessage.success('投票成功！')
  //   } else {
  //     ElMessage.error('投票失败，请重试')
  //   }
  // } catch (error) {
  //   ElMessage.error('投票请求失败')
  //   console.error(error)
  // }
}


const submitArgue = async () => {
  try {
    let response = await service.post('/argue', {
      widgetId: props.data.widgetId,
      submitted_assignment_id: props.data.submitted_assignment_id,
      title: props.data.title,
      content: argueContent.value,
    });
    router.push({name: `argue/${props.data.argue_id}`});
  } catch (error) {
    ElMessage.error("提交辩驳失败，请稍后重试");
  }
}

const submitArgueFeedback = () => {

}

// 评论数据
const comments = ref([
  {
    content: '这是一条示例评论！',
    author: '用户1',
  }
]);

// 新评论内容
const newComment = ref('');

// 发布新评论
const submitComment = () => {
  if (!newComment.value.trim()) return;
  
  const comment = {
    content: newComment.value,
    author: '当前用户',
  };
  
  comments.value.unshift(comment);
  newComment.value = '';
};

// 处理回复
const handleReply = (author: string) => {
  newComment.value = `@${author} `;
};

onMounted(async () => {
  argueContent.value = '';
  argueFileList.value = [];
  argueEditor.value?.updateContent(argueContent.value);
  argueFeedbackContent.value = '';
  argueFeedbackFileList.value = [];
  argueEditor.value?.updateContent(argueContent.value);
  isEditing.value = true;

  const role = getRoleByCourseId(props.data.courseId);
  // isTeacher.value = role === 'teacher' || role === 'admin';
  // isEditing.value = props.data.status === 'pending' &&
  //                   props.data.starter === localStorage.getItem('username');
  isEditing.value = true;
});
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

.toolbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 24px;
  background-color: transparent;
  padding: 10px 0;
  border-radius: 12px;
}

.follow-section, .score-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-section .el-input-number {
  width: 120px;
}

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

.Revised-score {
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
  