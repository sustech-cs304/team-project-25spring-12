<template>
    <widget-card :title="computedTitle" color="orange" icon="Opportunity">
      <div class="discussion-area">
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
          <el-card v-for="comment in comments" :key="comment.id" class="comment-item">
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
            <!-- <el-button type="text" v-if="comment.likes !== undefined">
              <el-icon><Star/></el-icon> {{ comment.likes }}
            </el-button> -->
            </div>
          </el-card>
        </div>
      </div>
    </widget-card>
  </template>
  
  <script setup lang="ts">
    import WidgetCard from "./utils/widget-card.vue";
    import {computed, ref, onMounted} from "vue";
    import axios from "axios";
    
    const props = defineProps({
      data: {
        type: Object,
        required: true,
      },
    });
    // 本卡片的标题
    const computedTitle = computed(() => props.data?.title || "帖子");
    
    import { Star } from '@element-plus/icons-vue'
    import { ElMessage } from 'element-plus'
    
    // 模拟评论数据
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
    
    // 可以在这里添加从API获取数据的逻辑
    onMounted(() => {
      // fetchPostAndComments()
    })
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