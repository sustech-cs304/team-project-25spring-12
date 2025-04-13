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
              @click="submitArgument"
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
          <el-col :span="6" class="edit-button">
            <el-button
                type="primary"
                link
                :icon="Edit"
                @click="editSubmittedArguement(props.data.submittedArguement)"
            >
              编辑
            </el-button>
          </el-col>
        </el-row>
        <div class="container">
          <md-and-file :fileList="props.data.submittedArguement.attachments" :content="props.data.submittedArguement.content"/>
        </div>
      </div>

      <!-- 投票结果 -->
      <div v-if="props.data.status !== 'pending'">
        <!-- <el-text class="section-title">投票结果</el-text> -->
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
            <el-button size="small" type="primary" disabled>{{ props.data.voteSupport }} / {{ props.data.voteTotal }}</el-button>
            </el-progress>
          </el-table-column>
          <el-table-column label="投票">
            <div style="display: flex; align-items: center">
              <!-- <el-button-group> -->
                <el-button onclick="vote(true)" type="success">支持</el-button>
                <el-button onclick="vote(false)" type="warning">反对</el-button>
              <!-- </el-button-group> -->
            </div>
          </el-table-column>
        </el-table>
      </div>

      <!-- 讨论区 -->
      <div v-if="props.data.status !== 'pending'">
        <el-text class="section-title">讨论区</el-text>
        <div class="discussion-area">
          <!-- 评论统计 -->
          <div class="comment-stats">
            评论数：{{ comments.length }}
          </div>

          <!-- 评论表单 -->
          <div class="comment-form">
            <h3>{{ replyToUser ? `回复 @${replyToUser}` : '发表评论' }}</h3>
            <el-input
              type="textarea"
              :rows="4"
              v-model="commentContent"
              placeholder="请输入你的评论..."
            ></el-input>
            <div class="form-actions">
              <el-button type="primary" @click="submitComment">提交</el-button>
              <el-button v-if="replyToUser" @click="cancelReply">取消回复</el-button>
            </div>
          </div>

          <!-- 评论列表 -->
          <div class="comment-list">
            <el-card v-for="comment in comments.reverse()" :key="comment.id" class="comment-item">
              <div class="comment-header">
              <el-avatar :size="40" :src="comment.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
              <div class="comment-user">
                <span class="username">{{ comment.username }}</span>
                <span class="time">{{ formatDate(comment.createdAt) }}</span>
              </div>
              </div>
              <div class="comment-content">
              {{ comment.content }}
              </div>
              <div class="comment-actions">
              <el-button type="text" @click="replyTo(comment)">回复</el-button>
              <el-button type="text" v-if="comment.likes !== undefined">
                <el-icon><Star/></el-icon> {{ comment.likes }}
              </el-button>
              </div>
            </el-card>
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
  import {Checked, Edit, Finished, Memo, Timer, Upload, Star} from "@element-plus/icons-vue";
  import { ElMessage } from 'element-plus'
  import axios from "axios";

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

  // 编辑提交记录
  const isEditing = ref(false);
  const content = ref("");
  const fileList = ref([]);
  const editSubmittedArguement = (record: any) => {
    content.value = JSON.parse(JSON.stringify(record.content));
    fileList.value = JSON.parse(JSON.stringify(record.attachments));
    // updateMode();
    isEditing.value = true;
  }
  
  // 提交辩驳
  const submitArgument = () => {
    
  }

  const editArgument = () =>{

  }

  const reviseArgument = () => {
    
  }

  const vote = (isSupport: boolean) => {
    axios.post(
      '/argue/vote',
      {
        argue_post_id: props.data.argueId,
        is_support: isSupport,
      },
    )
  }

  const comments = ref([
  {
    id: 1,
    username: '用户A',
    avatar: '',
    content: '这是一个很好的帖子，感谢分享！',
    createdAt: new Date(Date.now() - 3600000 * 2),
    likes: 5
  },
  {
    id: 2,
    username: '用户B',
    avatar: '',
    content: '我不同意作者的观点，我认为...',
    createdAt: new Date(Date.now() - 3600000),
    likes: 2
  }])
  
  const commentContent = ref('')
  const replyToUser = ref(null)
  const replyCommentId = ref(null)
  
  // 格式化日期
  const formatDate = (date) => {
    return new Date(date).toLocaleString()
  }
  
  // 回复评论
  const replyTo = (comment) => {
    replyToUser.value = comment.username
    replyCommentId.value = comment.id
    commentContent.value = `@${comment.username} `
  }
  
  // 取消回复
  const cancelReply = () => {
    replyToUser.value = null
    replyCommentId.value = null
  }
  
  // 提交评论
  const submitComment = () => {
    if (!commentContent.value.trim()) {
      ElMessage.warning('评论内容不能为空')
      return
    }
  
    const newComment = {
      id: comments.value.length + 1,
      username: '当前用户',
      avatar: '',
      content: commentContent.value,
      createdAt: new Date(),
      likes: 0
    }
  
    comments.value.push(newComment)
    commentContent.value = ''
    replyToUser.value = null
    replyCommentId.value = null
  
    ElMessage.success('评论发表成功')
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

  .discussion-area {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .post-card {
    margin-bottom: 20px;
  }
  
  .post-header h2 {
    margin: 0;
    padding: 0;
  }
  
  .post-meta {
    margin-top: 10px;
    font-size: 14px;
    color: #666;
  }
  
  .post-meta span {
    margin-right: 15px;
  }
  
  .post-content {
    line-height: 1.6;
  }
  
  .comment-stats {
    margin: 20px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
  }
  
  .comment-item {
    margin-bottom: 15px;
  }
  
  .comment-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .comment-user {
    margin-left: 10px;
    display: flex;
    flex-direction: column;
  }
  
  .username {
    font-weight: bold;
  }
  
  .time {
    font-size: 12px;
    color: #999;
  }
  
  .comment-content {
    margin-left: 50px;
    line-height: 1.5;
  }
  
  .comment-actions {
    margin-top: 10px;
    text-align: right;
  }
  
  .comment-form {
    margin-top: 30px;
  }
  
  .form-actions {
    margin-top: 15px;
    text-align: right;
  }
</style>
  