<template>
  <div class="admin-page">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 用户管理 -->
      <el-tab-pane label="用户管理" name="users">
        <div class="user-management">
          <div class="action-bar">
            <el-button type="primary" @click="openAddUserDialog">添加用户</el-button>
            <el-select v-model="userSearchType" style="width: 120px; margin-right: 10px">
              <el-option label="按姓名" value="name" />
              <el-option label="按用户名" value="username" />
              <el-option label="按部门" value="department" />
              <el-option label="按邮箱" value="email" />
            </el-select>
            <el-input
              v-model="userSearch"
              :placeholder="getUserSearchPlaceholder"
              style="width: 200px"
              clearable
              @input="filterUsers"
            />
          </div>
          <el-table
            :data="filteredUsers"
            style="width: 100%"
            border
            @sort-change="handleUserSortChange"
          >
            <el-table-column prop="username" label="用户名" sortable />
            <el-table-column prop="name" label="姓名" sortable />
            <el-table-column prop="department" label="部门" sortable />
            <el-table-column prop="email" label="邮箱" sortable />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="warning" size="small" @click="openEditUserDialog(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteUser(row.username)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 课程管理 -->
      <el-tab-pane label="课程管理" name="courses">
        <div class="course-management">
          <div class="action-bar">
            <el-button type="primary" @click="openAddCourseDialog">添加课程</el-button>
            <el-select v-model="semesterFilter" style="width: 150px; margin-right: 10px" placeholder="选择学期" clearable @change="filterCourses">
              <el-option
                v-for="semester in invertedSemesters"
                :key="semester.id"
                :label="semester.name"
                :value="semester.id"
              />
            </el-select>
            <el-select v-model="courseSearchType" style="width: 120px; margin-right: 10px">
              <el-option label="按课程名" value="name" />
              <el-option label="按课程代码" value="course_code" />
            </el-select>
            <el-input
              v-model="courseSearch"
              :placeholder="courseSearchType === 'course_code' ? '搜索课程代码' : '搜索课程名'"
              style="width: 200px"
              clearable
              @input="filterCourses"
            />
          </div>
          <el-table
            :data="filteredCourses"
            style="width: 100%"
            border
            @sort-change="handleCourseSortChange"
          >
            <el-table-column prop="semester_name" label="学期" width="100" sortable />
            <el-table-column prop="course_code" label="课程代码" sortable />
            <el-table-column prop="name" label="课程名" sortable />
            <el-table-column label="讲师">
              <template #default="{ row }">
                {{ getUserName(row.lecturer) }}
              </template>
            </el-table-column>
            <el-table-column label="助教">
              <template #default="{ row }">
                {{ getUserNames(row.assistants).join(', ') }}
              </template>
            </el-table-column>
            <el-table-column prop="location" label="地点" sortable />
            <el-table-column prop="time" label="时间" sortable />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="warning" size="small" @click="openEditCourseDialog(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteCourse(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 学期管理 -->
      <el-tab-pane label="学期管理" name="semesters">
        <div class="semester-management">
          <div class="action-bar">
            <el-button type="primary" @click="openAddSemesterDialog">添加学期</el-button>
            <el-input
              v-model="semesterSearch"
              placeholder="搜索学期名称"
              style="width: 200px"
              clearable
              @input="filterSemesters"
            />
          </div>
          <el-table
            :data="filteredSemesters"
            style="width: 100%"
            border
            @sort-change="handleSemesterSortChange"
          >
            <el-table-column prop="id" label="ID" width="100" sortable />
            <el-table-column prop="name" label="学期名称" sortable />
            <el-table-column prop="start_time" label="开始时间" sortable />
            <el-table-column prop="end_time" label="结束时间" sortable />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="warning" size="small" @click="openEditSemesterDialog(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteSemester(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      :title="userDialogTitle"
      v-model="userDialogVisible"
      width="30%"
      @close="resetUserForm"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="userForm.department" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑课程对话框 -->
    <el-dialog
      :title="courseDialogTitle"
      v-model="courseDialogVisible"
      width="30%"
      @close="resetCourseForm"
    >
      <el-form :model="courseForm" :rules="courseRules" ref="courseFormRef">
        <el-form-item label="学期" prop="semester">
          <el-select v-model="courseForm.semester" placeholder="选择学期">
            <el-option
              v-for="semester in invertedSemesters"
              :key="semester.id"
              :label="semester.name"
              :value="semester.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="课程代码" prop="course_code">
          <el-input v-model="courseForm.course_code" />
        </el-form-item>
        <el-form-item label="课程名" prop="name">
          <el-input v-model="courseForm.name" />
        </el-form-item>
        <el-form-item label="讲师" prop="lecturer">
          <el-select
            v-model="courseForm.lecturer"
            placeholder="选择讲师"
            filterable
            clearable
            style="width: 100%"
            :filter-method="filterUsers"
          >
            <el-option
              v-for="user in filteredUsersForCourse"
              :key="user.username"
              :label="user.name"
              :value="user.username"
            >
              <div class="user-option">
                <span class="user-name">{{ user.name }}</span>
                <span class="user-email">{{ user.email }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="助教" prop="assistants">
          <el-select
            v-model="courseForm.assistants"
            placeholder="选择助教"
            filterable
            clearable
            multiple
            style="width: 100%"
            :filter-method="filterUsers"
          >
            <el-option
              v-for="user in filteredUsersForCourse"
              :key="user.username"
              :label="user.name"
              :value="user.username"
            >
              <div class="user-option">
                <span class="user-name">{{ user.name }}</span>
                <span class="user-email">{{ user.email }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学生" prop="students">
          <el-select
            v-model="courseForm.students"
            placeholder="选择学生"
            filterable
            clearable
            multiple
            style="width: 100%"
            :filter-method="filterUsers"
          >
            <el-option
              v-for="user in filteredUsersForCourse"
              :key="user.username"
              :label="user.name"
              :value="user.username"
            >
              <div class="user-option">
                <span class="user-name">{{ user.name }}</span>
                <span class="user-email">{{ user.email }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="地点" prop="location">
          <el-input v-model="courseForm.location" type="textarea" />
        </el-form-item>
        <el-form-item label="时间" prop="time">
          <el-input v-model="courseForm.time" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="courseDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCourse">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑学期对话框 -->
    <el-dialog
      :title="semesterDialogTitle"
      v-model="semesterDialogVisible"
      width="30%"
      @close="resetSemesterForm"
    >
      <el-form :model="semesterForm" :rules="semesterRules" ref="semesterFormRef">
        <el-form-item label="学期名称" prop="name">
          <el-input v-model="semesterForm.name" />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-input v-model="semesterForm.start_time" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-input v-model="semesterForm.end_time" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="semesterDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSemester">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import service from '../../utils/request'

// 用户管理相关
const activeTab = ref('users')
const userSearch = ref('')
const userSearchType = ref('name')
const userDialogVisible = ref(false)
const userDialogTitle = ref('添加用户')
const userFormRef = ref(null)
const userForm = ref({
  name: '',
  username: '',
  department: '',
  email: ''
})
const userRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  department: [{ required: true, message: '请输入部门', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
  ]
}
const users = ref([
  { name: 'Admin User', username: 'admin', department: 'Administration', email: 'admin@example.com' },
  { name: 'Teacher One', username: 'teacher1', department: 'Mathematics', email: 'teacher1@example.com' },
  { name: 'Teacher Two', username: 'teacher2', department: 'Computer Science', email: 'teacher2@example.com' },
  { name: 'Student One', username: 'student1', department: 'Physics', email: 'student1@example.com' }
])
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    if (userSearchType.value === 'name') {
      return user.name.toLowerCase().includes(userSearch.value.toLowerCase())
    } else if (userSearchType.value === 'username') {
      return user.username.toLowerCase().includes(userSearch.value.toLowerCase())
    } else if (userSearchType.value === 'department') {
      return user.department.toLowerCase().includes(userSearch.value.toLowerCase())
    } else {
      return user.email.toLowerCase().includes(userSearch.value.toLowerCase())
    }
  })
})

const getUserSearchPlaceholder = computed(() => {
  switch (userSearchType.value) {
    case 'username':
      return '搜索用户名'
    case 'department':
      return '搜索部门'
    case 'email':
      return '搜索邮箱'
    default:
      return '搜索姓名'
  }
})

const openAddUserDialog = () => {
  userDialogTitle.value = '添加用户'
  userDialogVisible.value = true
}
const openEditUserDialog = (user) => {
  userDialogTitle.value = '编辑用户'
  userForm.value = { ...user }
  userDialogVisible.value = true
}
const resetUserForm = () => {
  userForm.value = { name: '', username: '', department: '', email: '' }
  userFormRef.value?.resetFields()
}
const saveUser = () => {
  userFormRef.value.validate((valid) => {
    if (valid) {
      const index = users.value.findIndex(u => u.username === userForm.value.username)
      if (index !== -1) {
        users.value[index] = { ...userForm.value }
        ElMessage.success('用户更新成功')
      } else {
        users.value.push({ ...userForm.value })
        ElMessage.success('用户添加成功')
      }
      userDialogVisible.value = false
    }
  })
}
const deleteUser = (username) => {
  service.delete(`/users/${username}`) // 嘻嘻后端现在没有这个接口
    .then(() => {
      users.value = users.value.filter(user => user.username !== username)
      ElMessage.success('用户删除成功')
    })
    .catch(() => {
      ElMessage.error('删除用户失败，请稍后重试')
    })
}

// 课程管理相关
const courseSearch = ref('')
const courseSearchType = ref('name')
const courseDialogVisible = ref(false)
const courseDialogTitle = ref('添加课程')
const courseFormRef = ref(null)
const courseForm = ref({
  id: null,
  semester: '',
  course_code: '',
  name: '',
  lecturer: '',
  assistants: [],
  students: [],
  location: '',
  time: ''
})
const courseRules = {
  semester: [{ required: true, message: '请选择学期', trigger: 'change' }],
  course_code: [{ required: true, message: '请输入课程代码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入课程名', trigger: 'blur' }],
  lecturer: [{ required: true, message: '请选择一名讲师', trigger: 'change' }],
  assistants: [{ required: false, type: 'array', trigger: 'change' }],
  students: [{ required: false, type: 'array', trigger: 'change' }],
  location: [{ required: false, message: '请输入课程地点', trigger: 'blur' }],
  time: [{ required: false, message: '请输入课程时间', trigger: 'blur' }]
}
const semesters = ref([
  { id: 1, name: '2023 春季', start_time: '2023-02-01', end_time: '2023-06-30' },
  { id: 2, name: '2023 秋季', start_time: '2023-09-01', end_time: '2024-01-31' },
  { id: 3, name: '2024 春季', start_time: '2024-02-01', end_time: '2024-06-30' },
  { id: 4, name: '2024 秋季', start_time: '2024-09-01', end_time: '2025-01-31' },
  { id: 5, name: '2025 春季', start_time: '2025-02-01', end_time: '2025-06-30' },
])
const semesterFilter = ref('')
const invertedSemesters = computed(() => {
  return [...semesters.value].sort((a, b) => b.id - a.id)
})

const courses = ref([
  { id: 1, course_code: "MA-101", name: '数学基础', semester: 1, lecturer: 'teacher1', assistants: ['student1'], students: ['student1'], location: 'Room 101', time: 'Mon 9:00-11:00' },
  { id: 2, course_code: "CS-101", name: '编程入门', semester: 2, lecturer: 'teacher1', assistants: ['student1'], students: ['student1'], location: 'Lab 305', time: 'Wed 14:00-16:00' },
])
const filteredCourses = computed(() => {
  return courses.value
    .filter(course => {
      const matchesSearch = courseSearchType.value === 'course_code'
        ? course.course_code.toString().includes(courseSearch.value)
        : course.name.toLowerCase().includes(courseSearch.value.toLowerCase())
      const matchesSemester = semesterFilter.value
        ? course.semester === semesterFilter.value
        : true
      return matchesSearch && matchesSemester
    })
    .map(course => ({
      ...course,
      semester_name: semesters.value.find(sem => sem.id === course.semester)?.name || '未知学期'
    }))
})

const filteredUsersForCourse = ref(users.value)

const filterUsers = (query) => {
  const lowerQuery = query.toLowerCase()
  filteredUsersForCourse.value = users.value.filter(user => 
    user.name.toLowerCase().includes(lowerQuery) || 
    user.username.toLowerCase().includes(lowerQuery) || 
    user.email.toLowerCase().includes(lowerQuery) ||
    user.department.toLowerCase().includes(lowerQuery)
  )
}

const getUserName = (username) => {
  const user = users.value.find(u => u.username === username)
  return user ? user.name : '未知用户'
}

const getUserNames = (usernames) => {
  return usernames.map(username => {
    const user = users.value.find(u => u.username === username)
    return user ? user.name : '未知用户'
  })
}

const openAddCourseDialog = () => {
  courseDialogTitle.value = '添加课程'
  courseDialogVisible.value = true
}
const openEditCourseDialog = (course) => {
  courseDialogTitle.value = '编辑课程'
  courseForm.value = { ...course }
  courseDialogVisible.value = true
}
const resetCourseForm = () => {
  courseForm.value = { id: null, name: '', semester: '', lecturer: '', assistants: [], students: [], location: '', time: '' }
  courseFormRef.value?.resetFields()
  filteredUsersForCourse.value = users.value
}
const saveCourse = () => {
  courseFormRef.value.validate((valid) => {
    if (valid) {
      if (courseForm.value.id) {
        const index = courses.value.findIndex(c => c.id === courseForm.value.id)
        courses.value[index] = { ...courseForm.value }
        ElMessage.success('课程更新成功')
      } else {
        courses.value.push({
          ...courseForm.value,
          id: courses.value.length + 1
        })
        ElMessage.success('课程添加成功')
      }
      courseDialogVisible.value = false
    }
  })
}
const deleteCourse = (id) => {
  service.delete(`/class/${id}`)
    .then(() => {
      courses.value = courses.value.filter(course => course.id !== id)
      ElMessage.success('课程删除成功')
    })
    .catch(() => {
      ElMessage.error('删除课程失败，请稍后重试')
    })
}
const filterCourses = () => {}

// 学期管理相关
const semesterSearch = ref('')
const semesterDialogVisible = ref(false)
const semesterDialogTitle = ref('添加学期')
const semesterFormRef = ref(null)
const semesterForm = ref({
  id: null,
  name: '',
  start_time: '',
  end_time: ''
})
const semesterRules = {
  name: [{ required: true, message: '请输入学期名称', trigger: 'blur' }],
  start_time: [{ required: true, message: '请输入开始时间', trigger: 'blur' }],
  end_time: [{ required: true, message: '请输入结束时间', trigger: 'blur' }]
}

const filteredSemesters = computed(() => {
  return semesters.value.filter(semester =>
    semester.name.toLowerCase().includes(semesterSearch.value.toLowerCase())
  )
})

const openAddSemesterDialog = () => {
  semesterDialogTitle.value = '添加学期'
  semesterDialogVisible.value = true
}

const openEditSemesterDialog = (semester) => {
  semesterDialogTitle.value = '编辑学期'
  semesterForm.value = { ...semester }
  semesterDialogVisible.value = true
}

const resetSemesterForm = () => {
  semesterForm.value = { id: null, name: '', start_time: '', end_time: '' }
  semesterFormRef.value?.resetFields()
}

const saveSemester = () => {
  semesterFormRef.value.validate((valid) => {
    if (valid) {
      if (semesterForm.value.id) {
        const index = semesters.value.findIndex(s => s.id === semesterForm.value.id)
        semesters.value[index] = { ...semesterForm.value }
        ElMessage.success('学期更新成功')
      } else {
        semesters.value.push({
          id: semesters.value.length + 1,
          name: semesterForm.value.name,
          start_time: semesterForm.value.start_time,
          end_time: semesterForm.value.end_time
        })
        ElMessage.success('学期添加成功')
      }
      semesterDialogVisible.value = false
    }
  })
}

const deleteSemester = (id) => {
  const isUsed = courses.value.some(course => course.semester === id)
  if (isUsed) {
    ElMessage.error('无法删除正在被课程使用的学期')
    return
  }
  service.delete(`/class/semester/${id}`)
    .then(() => {
      semesters.value = semesters.value.filter(semester => semester.id !== id)
      ElMessage.success('学期删除成功')
    })
    .catch(() => {
      ElMessage.error('删除学期失败，请稍后重试')
    })
}

const filterSemesters = () => {}
</script>

<style scoped>
.admin-page {
  padding: 20px;
}
.action-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}
.user-option {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.user-name {
  flex: 1;
  text-align: left;
}
.user-email {
  flex: 1;
  text-align: right;
  color: #909399;
}
</style>