<template>
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
      <el-button type="primary" @click="submitComment" :disabled="!newComment.trim()">发布评论</el-button>
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
</template>

<script setup>
import { ref } from 'vue';
import { ElInput, ElButton } from 'element-plus';

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
  newComment.value = `@${author} ${newComment.value}`.trim();
};
</script>

<style scoped>
.comment-section {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.comment-input {
  margin-bottom: 20px;
}

.comment-input .el-textarea {
  margin-bottom: 10px;
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
  margin-bottom: 10px;
}
</style>