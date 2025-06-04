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
            <span>学期: {{ activeCourse.semester }}</span>
            <span>教师: {{ activeCourse.lecturer }}</span>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div class="filter-container">
          <el-select
            v-model="selectedStudents"
            multiple
            filterable
            reserve-keyword
            collapse-tags
            collapse-tags-tooltip
            :max-collapse-tags="3"
            placeholder="搜索并选择学生"
            class="filter-select"
          >
            <el-option
              v-for="student in students"
              :key="student.username"
              :label="student.name"
              :value="student.username"
            >
              <div class="student-option">
                <span>{{ student.name }}</span>
              </div>
            </el-option>
          </el-select>

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
              v-for="assignment in assignments"
              :key="assignment.id"
              :label="assignment.title"
              :value="assignment.id"
            >
              <div class="assignment-option">
                <span>{{ assignment.title }}</span>
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
        <!-- 分数表格 -->
        <div class="score-table-container" v-if="filteredAssignments.length > 0 && filteredStudents.length > 0">
          <el-table
            :data="tableData"
            style="width: 100%"
            v-loading="tableLoading"
            border
            :empty-text="'未找到相关数据'"
          >
            <!-- 学生 -->
            <el-table-column
              prop="student"
              label="学生"
              min-width="180"
            >
              <template #default="{ row }">
                <div class="student-info">
                  <span class="student-name">{{ row.student.name }}</span>
                </div>
              </template>
            </el-table-column>
            <!-- 作业 -->
            <el-table-column
              prop="assignment"
              label="作业"
              min-width="160"
            >
              <template #default="{ row }">
                <div class="assignment-header">
                  <span class="assignment-title">{{ row.assignment.title }}</span>
                </div>
              </template>
            </el-table-column>
            <!-- 得分 -->
            <el-table-column
              prop="score"
              label="得分"
              width="120"
            >
              <template #default="{ row }">
                <div class="score-cell">
                  <span v-if="row.feedback">
                    {{ row.feedback.score }}<span v-if="row.assignment.maxScore"> / {{ row.assignment.maxScore }}</span>
                  </span>
                  <span v-else>
                    <el-tag size="small" type="info">未批改</el-tag>
                  </span>
                </div>
              </template>
            </el-table-column>
            <!-- 详情 -->
            <el-table-column
              label="详情"
              width="110"
              align="center"
            >
              <template #default="{ row }">
                <el-button
                  v-if="row.assignment.submitType === 'file'"
                  type="primary"
                  size="small"
                  plain
                  @click="handleFileDetail(row)"
                >查看详情</el-button>
                <el-button
                  v-else
                  type="primary"
                  size="small"
                  plain
                  @click="handleCodeDetail(row)"
                >查看详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 修改后的文件型详情对话框，支持“原地查看详情”并提供跳转按钮 -->
        <el-dialog
          v-model="fileDialogVisible"
          title="文件型作业提交详情"
          width="600px"
        >
          <div v-if="fileDetailRecord">
            <p><b>学生：</b>{{ fileDetailRecord.student?.name }} ({{ fileDetailRecord.student?.username }})</p>
            <p><b>提交时间：</b>{{ timestampToString(fileDetailRecord.submittedTime) }}</p>
            <div v-if="fileDetailRecord.attachments?.length">
              <b>附件：</b>
              <el-link
                v-for="file in fileDetailRecord.attachments"
                :key="file.id"
                @click="handleDownloadFile(file)"
                target="_blank"
                type="primary"
                style="margin-right: 10px"
              >{{ file.filename }}</el-link>
            </div>
            <div v-if="fileDetailRecord.content">
              <b>内容：</b>
              <div style="white-space: pre-wrap; background: #f5f7fa; padding: 8px; border-radius: 4px;">{{ fileDetailRecord.content }}</div>
            </div>
            <div v-if="fileDetailRecord.feedback">
              <hr />
              <p><b>评分：</b>{{ fileDetailRecord.feedback.score }}</p>
              <p><b>评语：</b></p>
              <div style="margin-bottom: 8px; white-space: pre-wrap;">{{ fileDetailRecord.feedback.content }}</div>
              <p><b>批改时间：</b>{{ timestampToString(fileDetailRecord.feedback.createTime) }}</p>
              <div v-if="fileDetailRecord.feedback.attachments?.length">
                <b>批改附件：</b>
                <el-link
                  v-for="file in fileDetailRecord.feedback.attachments"
                  :key="file.id"
                  @click="handleDownloadFile(file)"
                  target="_blank"
                  type="primary"
                  style="margin-right: 10px"
                >{{ file.filename }}</el-link>
              </div>
            </div>
            <div style="text-align: right; margin-top: 16px;">
              <el-button
                type="primary"
                @click="handleFileJump(fileDetailRecord)"
                size="small"
              >前往批改页面</el-button>
            </div>
          </div>
        </el-dialog>

        <!-- 代码详情对话框 -->
        <el-dialog
          v-model="codeDialogVisible"
          title="代码提交详情"
          width="600px"
        >
          <div v-if="detailRecord">
            <p><b>学生：</b>{{ detailRecord.student?.name }} ({{ detailRecord.student?.username }})</p>
            <p><b>提交时间：</b>{{ timestampToString(detailRecord.submittedTime) }}</p>
            <div v-if="detailRecord.code">
              <b>代码：</b>
              <el-tag size="small" style="margin-left: 8px">{{ detailRecord.code.language }}</el-tag>
              <pre style="background: #f8f8f8; padding: 12px; border-radius: 6px; margin-top: 8px; white-space: pre-wrap;">{{ detailRecord.code.code }}</pre>
            </div>
            <div v-if="detailRecord.feedback">
              <hr />
              <p><b>评分：</b>{{ detailRecord.feedback.score }}</p>
              <p><b>结果：</b></p>
              <md-preview :model-value="detailRecord.feedback.content"/>
              <p><b>批改时间：</b>{{ timestampToString(detailRecord.feedback.createTime) }}</p>
            </div>
          </div>
        </el-dialog>
      </div>

      <div v-else class="empty-tip">
        <el-icon :size="60"><InfoFilled /></el-icon>
        <p>请从左侧选择课程</p>
      </div>
    </el-main>
  </el-container>
</template>

<script setup lang="ts" name="grade-teacher">
import {ref, computed, onMounted} from "vue";
import {InfoFilled} from "@element-plus/icons-vue";
import type {Course} from "@/types/course";
import {ensureCoursesLoaded} from "@/composables/useUserData";
import {useUserStore} from "@/store/user";
import {SubmittedRecord} from "@/types/widgets";
import {useRoute, useRouter} from "vue-router";
import {getGradeCenter} from "@/api/feedback";
import {Grades} from "@/types/feedback";
import {MdPreview} from "md-editor-v3";
import "md-editor-v3/lib/preview.css";
import {useDownloader} from "@/composables/useDownloader";
import {ElMessage} from "element-plus";
import {FileMeta} from "@/types/fileMeta";

const route = useRoute();
const router = useRouter();
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

const assignments = ref<Grades[]>([]);
const selectedAssignments = ref<number[]>([]);
const filteredAssignments = computed(() => assignments.value.filter(assignment => selectedAssignments.value.length === 0 || selectedAssignments.value.includes(assignment.id)));

const students = computed(() => {
  const studentMap = new Map<string, any>();
  for (const assignment of assignments.value) {
    for (const submission of assignment.submissions) {
      const student = submission.student;
      if (student && !studentMap.has(student.username)) {
        studentMap.set(student.username, student);
      }
    }
  }
  return Array.from(studentMap.values());
});
const selectedStudents = ref<string[]>([]);
const filteredStudents = computed(() => students.value.filter(student => selectedStudents.value.length === 0 || selectedStudents.value.includes(student.username)));

// 表格加载状态
const tableLoading = ref(false);

// 处理学期变更
const handleSemesterChange = () => {
  activeCourseId.value = null;
};

// 处理课程选择
const handleCourseSelect = async (id: string) => {
  const courseId = Number(id);
  activeCourseId.value = Number(courseId);
  if (activeCourse.value) {
    try {
      tableLoading.value = true;
      const response = await getGradeCenter(courseId);
      assignments.value = response.data as Grades[];
      assignments.value.sort((a, b) => a.widgetId - b.widgetId);
    } catch (e) {
      console.error(e);
    } finally {
      tableLoading.value = false;
    }
  }
  // 重置筛选条件
  selectedStudents.value = [];
  selectedAssignments.value = [];
};

const initActiveCourse = () => {
  const id = route.query.course as string;
  const course = courses.value.find(course => course.id.toString() === id);
  if (course) {
    activeSemester.value = course.semester;
    handleCourseSelect(id);
  } else {
    activeSemester.value = sortedSemesters.value[0];
    activeCourseId.value = null;
  }
};

onMounted(async () => {
  await ensureCoursesLoaded();
  courses.value = userStore.courses!.filter(course => ["teacher", "teaching assistant"].includes(course.role));
  initActiveCourse();
});

/*
AI-generated-content
tool: GitHub Copilot
version: GPT-4.1
usage: generate a table
*/
// 表格数据整理
const tableData = computed(() => {
  // key: assignmentId-studentUsername, value: latest submission
  const map = new Map<string, any>();
  for (const assignment of filteredAssignments.value) {
    // 按学生分组
    const grouped = new Map<string, SubmittedRecord[]>();
    for (const submission of assignment.submissions) {
      if (
        submission.student &&
        filteredStudents.value.some(s => s.username === submission.student.username)
      ) {
        const arr = grouped.get(submission.student.username) || [];
        arr.push(submission);
        grouped.set(submission.student.username, arr);
      }
    }
    // 每个学生取最新一条
    for (const [username, arr] of grouped.entries()) {
      const latest = arr.reduce((a, b) =>
        new Date(a.submittedTime) > new Date(b.submittedTime) ? a : b
      );
      map.set(`${assignment.id}-${username}`, {
        assignment,
        student: latest.student,
        feedback: latest.feedback,
        record: latest,
      });
    }
  }
  return Array.from(map.values());
});

// 详情对话框相关
const fileDialogVisible = ref(false);
const fileDetailRecord = ref<SubmittedRecord | null>(null);
const fileDetailAssignment = ref<Grades | null>(null);
const codeDialogVisible = ref(false);
const detailRecord = ref<SubmittedRecord | null>(null);

function handleFileDetail(row: any) {
  fileDetailRecord.value = row.record;
  fileDetailAssignment.value = row.assignment; // 这里额外存 assignment
  fileDialogVisible.value = true;
}

function handleFileJump() {
  if (fileDetailRecord.value && fileDetailAssignment.value) {
    router.push({
      path: "/mark/" + activeCourseId.value + "/widget/" + fileDetailAssignment.value.widgetId,
      query: { submissionId: fileDetailRecord.value.id },
    });
  }
}

// 代码型详情弹窗
function handleCodeDetail(row: any) {
  detailRecord.value = row.record;
  codeDialogVisible.value = true;
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

.course-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #606266;
}

.course-credit {
  margin-right: 8px;
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

.student-option, .assignment-option {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.student-id, .assignment-date {
  color: #909399;
  font-size: 12px;
  margin-left: 10px;
}

.student-info {
  display: flex;
  flex-direction: column;
}

.student-name {
  font-weight: 500;
}

.student-id {
  font-size: 12px;
  color: #909399;
}

.assignment-header {
  display: flex;
  flex-direction: column;
  line-height: 1.4;
}

.assignment-title {
  font-weight: 500;
}

.assignment-deadline {
  font-size: 12px;
  color: #f56c6c;
}

.score-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 16px;
}

.score-table-container {
  margin-bottom: 32px;
}

.el-dialog__body {
  word-break: break-all;
}
</style>