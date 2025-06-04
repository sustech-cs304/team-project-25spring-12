<template>
  <div class="overall_container">
    <!-- 工具栏：关注按钮和打分框 -->
    <div class="toolbar" v-if="props.data.status != 'pending'">
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
              ref="argueEditor"
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
            提交时间：{{ props.data.submitTime }}
          </el-text>
        </el-col>
      </el-row>
      <div class="container">
        <!-- <md-and-file
          :fileList="argueFileList"
          :content="argueContent"
        /> -->
      </div>
    </div>

    <!-- 教师编辑辩驳反馈 -->
    <div v-if="isTeacher">
      <el-text class="section-title">编辑辩驳反馈</el-text>
      <div class="container">
        <!-- <md-and-file-editor
          :fileList="argueFeedbackFileList"
          :content="argueFeedbackContent"
          ref="argueFeedbackEditor"
          @upload="handleArgueFeedbackAttachmentUpload"
          @remove="handleArgueFeedbackAttachmentRemove"
        /> -->
      </div>
    </div>

    <!-- 辩驳反馈 -->
    <div v-if="props.data.status === 'returned' && !isTeacher">
      <el-text class="section-title">辩驳反馈</el-text>
      <div class="container">
        <!-- <md-and-file
          :fileList="props.data.argueFeedbackFilelist"
          :content="props.data.argueFeedbackContent"
        /> -->
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
</template>


<script setup lang="ts">
import { onMounted, ref } from "vue"
import { ElMessage } from "element-plus"
import argue from "../widgets/argue.vue"
import service from '../../utils/request';
import {useRoute} from "vue-router"

const argueData = ref({})
const argueId = ref(0);

const argueDataSubmitted = ref({
  title: 'ArgueSubmitted',
  content: '# 要Argue的作业\n\n你觉得老师批改有误',
  attachments: [
    {filename: '您的提交.pdf', url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip'},
  ],
  status: 'submitted',
  submitType: 'file',
  originalScore: 90,
  revisedScore: 85,
  maxScore: 100,

  submittedArguement: {
      attachments: [
        {
          filename: '您的争辩附件.pdf',
          url: 'https://ri-sycdn.kuwo.cn/c402c52983f7a06060cc9403927d09e1/67f66f89/resource/n2/55/73/2708435384.mp3?bitrate$128&from=vip',
        },
      ],
      content: "# This is my kingdom come↑\n\nThis is my kingdom come↓",
      time: "2025-03-14 11:45:16",
  },

  voteTotal: 0,
  voteSupport: 0,

  comments: [],

})

const argueDataReturned = ref({
  title: 'ArgueReturned',
  content: '# 要Argue的作业\n\n你觉得老师批改有误',
  status: 'returned',
  submitType: 'file',
  originalScore: 90,
  revisedScore: 85,
  maxScore: 100,

  voteTotal: 0,
  voteSupport: 0,

  comments: [],
})

onMounted(async () => {
  // try {
  //   argueId.value = Number(useRoute().params.argueId);
  //   const response = await service.get(`/argue/${argueId}`);
  // } catch (error) {
  //   ElMessage.error("加载争辩数据失败，请稍后重试")
  // }
})
</script>


<style scoped>
  .page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
</style>
