<template>
  <div class="widget-layout">
    <!-- 左侧菜单 -->
    <div class="widget-menu-wrapper" :class="{ collapsed }">
      <!-- 折叠按钮 -->
      <div class="menu-toggle" @click="toggleCollapse">
        <el-icon>
          <component :is="collapsed ? 'ArrowRightBold' : 'ArrowLeftBold'"/>
        </el-icon>
        <span v-if="showTitle" class="menu-title">提交记录</span>
      </div>

      <!-- 文件夹菜单 -->
      <el-menu
          class="widget-menu"
          :default-active="activeSubmissionId?.toString()"
          :collapse="collapsed"
          :collapse-transition="true"
          mode="vertical"
          @select="handleMenuSelect"
      >
        <el-menu-item
            v-for="submission in submissionsSorted"
            :key="submission.id"
            :index="submission.id.toString()"
            class="hoverable-item"
            :style="getMenuItemStyle(submission)"
            @mouseenter="hoveredSubmissionId = submission.id.toString()"
            @mouseleave="hoveredSubmissionId = null"
        >
          <el-icon>
            <DocumentChecked v-if="submission.feedback" />
            <Document v-else />
          </el-icon>
          <div v-if="!collapsed" class="submission-info">
            <div class="student-name">{{ submission.student?.name || "未知用户" }}</div>
            <div class="submission-time">{{ formatTime(submission.submittedTime) }}</div>
          </div>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主体内容区域 -->
    <div class="widget-content">
      <el-scrollbar>
        <assignment-mark
            v-if="activeSubmission !== undefined"
            :submission="activeSubmission"
            :feedback="activeFeedback"
            :max-score="maxScore"
            :blob-list="blobs"
            :patch="patch"
            @update-file="handleUpdateFile"
            @save="handleSave"
            @submit="handleSubmit"
        />
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts" name="mark">
import assignmentMark from "../widgets/assignment-mark.vue";
import {computed, nextTick, onMounted, ref, watch} from "vue";
import {FeedbackForm, SubmissionForMark} from "@/types/feedback";
import {useRoute} from "vue-router";
import {useUserStore} from "@/store/user";
import {getAllSubmissions} from "@/api/feedback";
import {downloadFile} from "@/api/file";
import {useFeedback} from "@/composables/useFeedback";

const route = useRoute();
const userStore = useUserStore();
const {createFeedback, updateFeedback} = useFeedback();

const submissions = ref<SubmissionForMark[]>([]);
const submissionsSorted = computed(() => [...submissions.value].sort((a, b) => {
  return a.id > b.id ? -1 : 1;
}));
const feedbacks = ref<Record<number, FeedbackForm>>({});
const blobs = ref<Record<string, Blob>>({});
const patch = ref<Record<string, Uint8Array>>({});

// TODO: set max score
const maxScore = ref(100);

const activeSubmissionId = ref<number | null>(null);
const hoveredSubmissionId = ref<string | null>(null);
const activeSubmission = computed(() => submissions.value.find(s => s.id === activeSubmissionId.value));
const activeFeedback = computed(() => feedbacks.value[Number(activeSubmissionId.value)]);

const collapsed = ref(false);
const showTitle = ref(true);
const toggleCollapse = async () => {
  collapsed.value = !collapsed.value;
  await nextTick();
};
watch(collapsed, (val) => {
  if (val) {
    showTitle.value = false;
  } else {
    setTimeout(() => {
      showTitle.value = true;
    }, 300);
  }
});

const getMenuItemStyle = (submission: SubmissionForMark) => {
  const isActive = submission.id === activeSubmissionId.value;
  const isHovered = submission.id.toString() === hoveredSubmissionId.value;
  const baseColor = '#f9f9f9'
  const hoverColor = '#e6f0ff'
  const activeColor = '#409eff'
  return {
    backgroundColor: isActive ? activeColor : (isHovered ? hoverColor : baseColor),
    color: isActive ? 'white' : 'black',
    fontWeight: 'bold',
    borderRadius: '6px',
    margin: '4px 8px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    justifyContent: collapsed.value ? 'center' : 'flex-start',
    transition: 'all 0.2s',
    cursor: 'pointer',
  }
}

const formatTime = (time: string) => {
  if (!time) {
    return "无提交时间";
  }
  return new Date(time).toLocaleString();
};

const initActiveSubmission = () => {
  const id = route.query.submissionId as string;
  const matched = submissions.value.find((s) => s.id.toString() === id);
  if (matched) {
    activeSubmissionId.value = matched.id;
  } else {
    activeSubmissionId.value = submissionsSorted.value[0].id;
  }
  updateBlobList(activeSubmissionId.value);
};

const handleMenuSelect = (submissionId: string) => {
  activeSubmissionId.value = Number(submissionId);
  updateBlobList(Number(submissionId));
};

const updateBlobList = (submissionId: number) => {
  blobs.value = {};
  const submission = submissionsSorted.value.find(s => s.id === submissionId);
  if (submission === undefined) {
    console.error(`Submission ${submissionId} is not found`);
    return;
  }
  const files = submission.feedback?.attachments || submission.attachments;
  if (files) {
    files.forEach(async (file) => {
      const response = await downloadFile(file.id);
      if (submissionId === activeSubmissionId.value) {
        blobs.value[file.id] = response.data as Blob;
      }
    });
  }
};

const handleUpdateFile = async (fileId: string, dataPromise: Promise<Uint8Array>) => {
  patch.value[fileId] = await dataPromise;
};

const handleSave = (submissionId: number, score?: number, content?: string) => {
  const feedback = feedbacks.value[submissionId];
  feedback.score = score;
  feedback.content = content;
};

const handleSubmit = async (submissionId: number, score: number, content: string) => {
  const submission = submissions.value.find((s) => s.id === submissionId);
  if (!submission) {
    console.error(`no such submission: ${submissionId}`);
    return;
  }
  const feedback = feedbacks.value[submissionId];
  feedback.score = score;
  feedback.content = content;
  if (!submission.feedback) {
    submission.feedback = await createFeedback(submission, feedback, patch.value);
  } else {
    submission.feedback = await updateFeedback(submission, feedback, patch.value);
  }
};

onMounted(async () => {
  const widgetId = route.params.widgetId as string;
  const response = await getAllSubmissions(widgetId);
  submissions.value = response.data as SubmissionForMark[];
  submissions.value.forEach(submission => {
    if (submission.feedback) {
      feedbacks.value[submission.id] = {
        score: submission.feedback.score,
        content: submission.feedback.content,
      };
    } else {
      feedbacks.value[submission.id] = {};
    }
  });
  initActiveSubmission();
});
</script>

<style scoped>
.widget-layout {
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.widget-menu {
  height: 100%;
}

.widget-menu-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid #ebeef5;
  transition: width 0.3s ease-in-out;
  width: 300px;
  flex-shrink: 0;
}

.widget-menu-wrapper.collapsed {
  width: 64px;
}

:deep(.el-menu--collapse) {
  width: 64px;
}

.menu-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid #ebeef5;
  transition: padding 0.3s ease-in-out;
}

.menu-title {
  font-weight: bold;
  font-size: 16px;
  transition: opacity 0.3s ease;
  white-space: nowrap;
}

.hoverable-item:hover {
  filter: brightness(1.08);
  cursor: pointer;
}

.widget-content {
  flex: 1;
  height: 100%;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden;
}

.widget-scroll-wrapper {
  height: 100%;
  overflow: auto;
}

.submission-info {
  display: flex;
  flex-direction: column;
  line-height: normal;
}

.student-name {
  font-size: 14px;
}

.submission-time {
  font-size: 12px;
  color: #909399;
}

.el-menu-item.is-active .submission-info .submission-time {
  color: white;
}
</style>
