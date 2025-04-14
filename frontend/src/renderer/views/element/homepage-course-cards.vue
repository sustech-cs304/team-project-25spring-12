<template>
  <div class="main-container">
    <el-tabs v-model="activeSemester" type="border-card" tab-position="left" style="height: 100%;">
      <el-tab-pane
          v-for="semester in sortedSemesters"
          :key="semester"
          :label="semester"
          :name="semester"
      >
        <el-scrollbar max-height="800px" wrap-style="padding-right: 4px;">
          <div class="course-scroll">
            <el-card
                v-for="course in coursesBySemester[semester]"
                :key="course.id"
                shadow="hover"
                class="course-card"
            >
              <div class="card-header">
                <div class="course-title">{{ course.courseCode }} - {{ course.name }}</div>
                <div class="course-semester">{{ course.semester }}</div>
              </div>

              <div class="card-body">
                <div class="course-info">
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>授课教师：{{ course.lecturer }}</span>
                </div>
                <div class="course-info">
                  <el-icon>
                    <Place/>
                  </el-icon>
                  <span>授课地点：{{ course.location }}</span>
                </div>
                <div class="course-info">
                  <el-icon>
                    <Timer/>
                  </el-icon>
                  <span>授课时间：{{ course.time }}</span>
                </div>
                <div class="course-info">
                  <el-icon>
                    <Avatar/>
                  </el-icon>
                  <span>您在本课程作为：{{ roleDisplayMap[course.role] }}</span>
                </div>
              </div>

              <div class="card-footer">
                <el-button type="primary" icon="Right" @click="enterCourse(course.id)">进入课程</el-button>
              </div>
            </el-card>
          </div>
        </el-scrollbar>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {Avatar, Place, Timer, User} from '@element-plus/icons-vue'
import type {Course} from "@/types/course";
import {useUserStore} from "@/store/user";
import {getCourses} from "@/api/course";
import {useRouter} from "vue-router";

const roleDisplayMap: Record<Course['role'], string> = {
  student: 'Student',
  teacher: 'Teacher',
  ta: 'Teaching Assistant'
}

const router = useRouter()
const userStore = useUserStore()
const courses = ref<Course[]>([])
const activeSemester = ref('')

onMounted(async () => {
  try {
    const response = await getCourses()
    const data: Course[] = response.data as Course[]
    userStore.setCourses(data)
    courses.value = data
    activeSemester.value = sortedSemesters.value[0] || ''
  } catch (err) {
    console.error('获取课程失败', err)
  }
})

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

const coursesBySemester = computed(() => {
  const map: Record<string, Course[]> = {}
  for (const course of courses.value) {
    if (!map[course.semester]) {
      map[course.semester] = []
    }
    map[course.semester].push(course)
  }
  return map
})

const enterCourse = (id: string) => {
  router.push('/course/' + id)
}
</script>

<style scoped>
.main-container {
  height: calc(100vh - 250px);
}

.course-scroll {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 12px 0;
}

.course-card {
  height: 180px;
  padding: 16px;
  width: 90%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.course-title {
  font-size: 18px;
  font-weight: bold;
  color: var(--el-text-color-primary);
}

.course-semester {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 4px;
}

.course-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}
</style>