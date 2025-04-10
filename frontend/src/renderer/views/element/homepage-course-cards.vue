<template>
  <el-tabs class="semester-tabs" v-model="activeSemester" type="border-card" tab-position="left">
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
                <el-icon><User /></el-icon>
                <span>授课教师：{{ course.lecturer }}</span>
              </div>
              <div class="course-info">
                <el-icon><Place /></el-icon>
                <span>授课地点：{{ course.location }}</span>
              </div>
              <div class="course-info">
                <el-icon><Timer /></el-icon>
                <span>授课时间：{{ course.time }}</span>
              </div>
              <div class="course-info">
                <el-icon><Avatar /></el-icon>
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
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { User, Place, Timer, Avatar } from '@element-plus/icons-vue'

interface Course {
  id: string
  courseCode: string
  name: string
  semester: string
  location: string
  time: string
  lecturer: string
  role: 'student' | 'teacher' | 'ta'
}

const roleDisplayMap: Record<Course['role'], string> = {
  student: 'Student',
  teacher: 'Teacher',
  ta: 'Teaching Assistant'
}

const courses = ref<Course[]>([
  {
    id: '1',
    courseCode: 'CS101',
    name: 'Intro to Programming',
    semester: '2025 Fall',
    location: 'Room A101',
    time: 'Mon 10:00-11:30',
    lecturer: 'Dr. Alice',
    role: 'student'
  },
  {
    id: '2',
    courseCode: 'CS202',
    name: 'Data Structures',
    semester: '2025 Summer',
    location: 'Room B201',
    time: 'Tue 14:00-15:30',
    lecturer: 'Prof. Bob',
    role: 'ta'
  },
  {
    id: '3',
    courseCode: 'CS303',
    name: 'Algorithms',
    semester: '2024 Fall',
    location: 'Room C301',
    time: 'Wed 10:00-11:30',
    lecturer: 'Dr. Charlie',
    role: 'teacher'
  },
  {
    id: '3',
    courseCode: 'CS309',
    name: 'Algorithms',
    semester: '2025 Fall',
    location: 'Room C301',
    time: 'Wed 10:00-11:30',
    lecturer: 'Dr. Charlie',
    role: 'teacher'
  }
])

const getSemesterValue = (semester: string): number => {
  const [yearStr, season] = semester.split(' ')
  const year = parseInt(yearStr)
  const seasonRank: Record<string, number> = { Spring: 1, Summer: 2, Fall: 3 }
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

const activeSemester = ref(sortedSemesters.value[0] || '')

const enterCourse = (id: string) => {
  // TODO: 跳转课程详情页
}
</script>

<style scoped>
.semester-tabs {
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