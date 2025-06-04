<!--
AI-generated-content
tool: DeepSeek
version: DeepSeek-R1-0528
usage: generate a draft, modified based on data format
-->

<template>
  <el-container style="height: 100%;">
    <!-- 左侧菜单 -->
    <el-aside width="280px" class="course-aside">
      <!-- 学期选择 -->
      <div class="semester-selector">
        <el-select
            v-model="activeSemester"
            placeholder="选择学期"
            size="large"
            class="semester-select"
            @change="handleSemesterChange"
        >
          <el-option
              v-for="semester in sortedSemesters"
              :key="semester"
              :label="semester"
              :value="semester"
          />
        </el-select>
      </div>

      <!-- 课程列表 -->
      <el-menu
          :default-active="activeCourseId?.toString()"
          @select="handleCourseSelect"
          class="course-menu"
      >
        <el-menu-item
            v-for="course in filteredCourses"
            :key="course.id"
            :index="course.id.toString()"
        >
          <div class="course-item">
            <span class="course-name">{{ course.name }}</span>
          </div>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-main class="score-main">
      <div v-if="activeCourse">
        <!-- 课程信息标题 -->
        <div class="course-header">
          <h2>{{ activeCourse.name }}</h2>
          <div class="course-meta">
            <span>课程编号: {{ activeCourse.courseCode }}</span>
            <span>学期: {{ activeCourse.semester }}</span>
            <span>教师: {{ activeCourse.lecturer }}</span>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div class="filter-container">
          <el-select
              v-model="selectedAssignments"
              multiple
              filterable
              reserve-keyword
              collapse-tags
              collapse-tags-tooltip
              :max-collapse-tags="3"
              placeholder="搜索并选择作业"
              class="filter-select"
          >
            <el-option
                v-for="assignment in sortedAssignments"
                :key="assignment.id"
                :label="assignment.title"
                :value="assignment.id"
            >
              <div class="assignment-option">
                <span>{{ assignment.title }}</span>
                <span class="assignment-date">(截止: {{ timestampToString(assignment.ddl) }})</span>
              </div>
            </el-option>
          </el-select>
        </div>

        <!--
        AI-generated-content
        tool: GitHub Copilot
        version: GPT-4.1
        usage: generate a table
        -->
        <div class="score-table-container" v-if="filteredAssignments.length > 0">
          <el-table
              :data="filteredAssignments"
              style="width: 100%"
              v-loading="tableLoading"
              border
              :empty-text="selectedAssignments.length > 0 ? '未找到相关作业' : '请筛选作业'"
          >
            <el-table-column
                prop="title"
                label="作业名称"
                min-width="180"
            >
              <template #default="{ row }">
                <span>{{ row.title }}</span>
              </template>
            </el-table-column>

            <el-table-column
                prop="ddl"
                label="截止时间"
                min-width="150"
            >
              <template #default="{ row }">
                <span>{{ timestampToString(row.ddl) }}</span>
              </template>
            </el-table-column>

            <el-table-column
                prop="status"
                label="提交状态"
                min-width="100"
            >
              <template #default="{ row }">
                <el-tag v-if="row.status === 'returned'" type="success">已批改</el-tag>
                <el-tag v-else-if="row.status === 'submitted'" type="warning">已提交</el-tag>
                <el-tag v-else type="info">未提交</el-tag>
              </template>
            </el-table-column>

            <el-table-column
                prop="score"
                label="得分"
                min-width="100"
            >
              <template #default="{ row }">
                <span v-if="row.status === 'returned'">
                  {{ row.feedback?.score ?? row.score }} / {{ row.maxScore }}
                </span>
                <span v-else-if="row.status === 'submitted'">
                  <el-tag size="small" type="warning">待批改</el-tag>
                </span>
                <span v-else>
                  <el-tag size="small" type="info">未提交</el-tag>
                </span>
              </template>
            </el-table-column>

            <el-table-column
                label="评语"
                min-width="220"
            >
              <template #default="{ row }">
                <span v-if="row.status === 'returned'">
                  {{ row.submitType === 'file' ? row.feedback?.content || '无评语' : '--' }}
                </span>
                <span v-else>--</span>
              </template>
            </el-table-column>

            <el-table-column
                label="操作"
                min-width="100"
                align="center"
            >
              <template #default="{ row }">
                <el-button
                    v-if="row.status === 'returned' && row.feedback"
                    type="primary"
                    size="small"
                    @click="handleViewFeedback(row)"
                    plain
                >查看详情
                </el-button>
                <el-button
                    v-else-if="row.status === 'submitted'"
                    type="success"
                    size="small"
                    @click="handleViewSubmission(row)"
                    plain
                >查看提交
                </el-button>
                <span v-else>--</span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 反馈弹窗 -->
        <el-dialog
          v-model="feedbackDialogVisible"
          title="作业反馈详情"
          width="600px"
        >
          <div v-if="currentSubmission && currentFeedback">
            <p><b>提交时间：</b>{{ timestampToString(currentSubmission.submittedTime) }}</p>
            <div v-if="currentSubmission.attachments?.length">
              <b>附件：</b>
              <el-link
                v-for="file in currentSubmission.attachments"
                :key="file.id"
                @click="handleDownloadFile(file)"
                target="_blank"
                type="primary"
                style="margin-right: 10px"
              >{{ file.filename }}</el-link>
            </div>
            <div v-if="currentSubmission.code">
              <b>代码：</b>
              <el-tag size="small" style="margin-left: 8px">{{ currentSubmission.code.language }}</el-tag>
              <pre style="background: #f8f8f8; padding: 12px; border-radius: 6px; margin-top: 8px; white-space: pre-wrap;">{{ currentSubmission.code.code }}</pre>
            </div>
            <div v-else>
              <b>内容：</b>
              <md-preview :model-value="currentSubmission.content" />
            </div>
            <hr />
            <p><b>批改时间：</b>{{ timestampToString(currentFeedback.createTime) }}</p>
            <div v-if="currentFeedback.attachments?.length">
              <b>批改附件：</b>
              <el-link
                v-for="file in currentFeedback.attachments"
                :key="file.id"
                @click="handleDownloadFile(file)"
                target="_blank"
                type="primary"
                style="margin-right: 10px"
              >{{ file.filename }}</el-link>
            </div>
            <p><b>评分：</b>{{ currentFeedback.score }}</p>
            <p><b>评语：</b></p>
            <md-preview :model-value="currentFeedback.content"/>
          </div>
        </el-dialog>

        <!-- 提交记录弹窗 -->
        <el-dialog
          v-model="submissionDialogVisible"
          title="作业提交详情"
          width="600px"
        >
          <div v-if="currentSubmission">
            <p><b>提交时间：</b>{{ timestampToString(currentSubmission.submittedTime) }}</p>
            <div v-if="currentSubmission.attachments?.length">
              <b>附件：</b>
              <el-link
                v-for="file in currentSubmission.attachments"
                :key="file.id"
                @click="handleDownloadFile(file)"
                target="_blank"
                type="primary"
                style="margin-right: 10px"
              >{{ file.filename }}</el-link>
            </div>
            <div v-if="currentSubmission.code">
              <b>代码：</b>
              <el-tag size="small" style="margin-left: 8px">{{ currentSubmission.code.language }}</el-tag>
              <pre style="background: #f8f8f8; padding: 12px; border-radius: 6px; margin-top: 8px; white-space: pre-wrap;">
        {{ currentSubmission.code.code }}</pre>
            </div>
            <div v-else>
              <b>内容：</b>
              <div style="white-space: pre-wrap;">{{ currentSubmission.content }}</div>
            </div>
          </div>
        </el-dialog>
      </div>

      <div v-else class="empty-tip">
        <el-icon :size="60">
          <InfoFilled/>
        </el-icon>
        <p>请从左侧选择课程</p>
      </div>
    </el-main>
  </el-container>
</template>

<script setup lang="ts" name="grade-student">
import {computed, onMounted, ref} from "vue";
import {InfoFilled} from "@element-plus/icons-vue";
import type {Course} from "@/types/course";
import {ensureCoursesLoaded} from "@/composables/useUserData";
import {useUserStore} from "@/store/user";
import {AssignmentWidget, Feedback, SubmittedRecord} from "@/types/widgets";
import {useRoute} from "vue-router";
import {getAllAssignments} from "@/api/feedback";
import {ElMessage} from "element-plus";
import {useDownloader} from "@/composables/useDownloader";
import {FileMeta} from "@/types/fileMeta";
import {MdPreview} from "md-editor-v3";
import "md-editor-v3/lib/preview.css";

const route = useRoute();
const userStore = useUserStore();

const {download} = useDownloader();

// 下载文件
const handleDownloadFile = async (file: FileMeta) => {  // 本项目中，目前 file.url 为空
  try {
    await download(file);
  } catch (error) {
    ElMessage.error("下载失败，请稍后重试");
  }
};

const timestampToString = (timestamp: string) => {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(timestamp));
};

const courses = ref<Course[]>([]);

const getSemesterValue = (semester: string): number => {
  const [yearStr, season] = semester.split(' ')
  const year = parseInt(yearStr)
  const seasonRank: Record<string, number> = {Spring: 1, Summer: 2, Fall: 3}
  return year * 10 + seasonRank[season] || 0
}

const sortedSemesters = computed(() => {
  const unique = [...new Set(courses.value.map(c => c.semester))]
  return unique.sort((a, b) => getSemesterValue(b) - getSemesterValue(a))
})

const activeSemester = ref<string>();

const filteredCourses = computed(() => courses.value.filter(course => course.semester === activeSemester.value));

const activeCourseId = ref<number | null>();
const activeCourse = computed(() => courses.value.find(course => course.id === activeCourseId.value));

const assignments = ref<AssignmentWidget[]>([]);
const sortedAssignments = computed(() => [...assignments.value].sort((a, b) => a.id - b.id));
const selectedAssignments = ref<number[]>([]);
const filteredAssignments = computed(() => sortedAssignments.value.filter(assignment => selectedAssignments.value.length === 0 || selectedAssignments.value.includes(assignment.id)));

// 表格加载状态
const tableLoading = ref(false);

// 处理学期变更
const handleSemesterChange = () => {
  activeCourseId.value = null;
  assignments.value = [];
  selectedAssignments.value = [];
}

// 处理课程选择
const handleCourseSelect = async (id: string) => {
  const courseId = Number(id);
  selectedAssignments.value = [];
  activeCourseId.value = courseId;
  if (activeCourse.value) {
    try {
      tableLoading.value = true;
      const response = await getAllAssignments(courseId);
      assignments.value = response.data as AssignmentWidget[];
      console.log(assignments.value);
    } catch (e) {
      console.error(e);
    } finally {
      tableLoading.value = false;
    }
  }
}

const initActiveCourse = () => {
  const id = route.query.course as string;
  const course = courses.value.find(course => course.id.toString() === id);
  if (course) {
    activeSemester.value = course.semester;
    handleCourseSelect(id);
  } else {
    activeSemester.value = sortedSemesters.value[0];
    handleSemesterChange();
  }
};

onMounted(async () => {
  await ensureCoursesLoaded();
  courses.value = userStore.courses!.filter(course => "student" === course.role);
  initActiveCourse();
})

/*
AI-generated-content
tool: GitHub Copilot
version: GPT-4.1
usage: generate a table
*/

// 反馈弹窗相关
const feedbackDialogVisible = ref(false);
const currentFeedback = ref<Feedback | null>(null);

function handleViewFeedback(row: AssignmentWidget) {
  const records = row.submittedAssignment ?? [];
  if (row.feedback) {
    currentSubmission.value = records.reduce((a, b) => new Date(a.submittedTime) > new Date(b.submittedTime) ? a : b);
    console.log(currentSubmission.value);
    currentFeedback.value = row.feedback;
    feedbackDialogVisible.value = true;
  } else {
    ElMessage.info('暂无反馈信息');
  }
}

// 提交记录弹窗相关
const submissionDialogVisible = ref(false);
const currentSubmission = ref<SubmittedRecord | null>(null);

function handleViewSubmission(row: AssignmentWidget) {
  // 取最新一条提交记录
  const records = row.submittedAssignment ?? [];
  if (records.length > 0) {
    // 假设按提交时间升序，取最后一条
    currentSubmission.value = records.reduce((a, b) => new Date(a.submittedTime) > new Date(b.submittedTime) ? a : b);
    submissionDialogVisible.value = true;
  } else {
    ElMessage.info('暂无提交记录');
  }
}
</script>

<style scoped>
.course-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e6e6e6;
  display: flex;
  flex-direction: column;
}

.semester-selector {
  padding: 20px 15px 15px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
}

.semester-select {
  width: 100%;
}

.course-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
}

.course-item {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.course-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.score-main {
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.course-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.course-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.course-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #606266;
}

.filter-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-select {
  flex: 1;
  min-width: 300px;
}

.empty-tip {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
  font-size: 16px;
}

.assignment-option {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.assignment-date {
  color: #909399;
  font-size: 12px;
  margin-left: 10px;
}

.score-table-container {
  margin-bottom: 32px;
}

.el-dialog__body {
  word-break: break-all;
}
</style>