<template>
  <div class="admin-page">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 用户管理 -->
      <el-tab-pane label="用户管理" name="users">
        <div class="user-management">
          <div class="action-bar">
            <el-button type="primary" @click="openAddUserDialog">添加用户</el-button>
            <el-input
              v-model="userSearch"
              placeholder="搜索用户名"
              style="width: 200px"
              clearable
              @input="filterUsers"
            />
          </div>
          <el-table :data="filteredUsers" style="width: 100%" border>
            <el-table-column prop="id" label="ID" width="100" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="role" label="角色" />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="warning" size="small" @click="openEditUserDialog(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteUser(row.id)">删除</el-button>
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
            <el-input
              v-model="courseSearch"
              placeholder="搜索课程名"
              style="width: 200px"
              clearable
              @input="filterCourses"
            />
          </div>
          <el-table :data="filteredCourses" style="width: 100%" border>
            <el-table-column prop="id" label="ID" width="100" />
            <el-table-column prop="name" label="课程名" />
            <el-table-column label="讲师">
              <template #default="{ row }">
                {{ row.instructor.join(', ') }}
              </template>
            </el-table-column>
            <el-table-column label="助教">
              <template #default="{ row }">
                {{ row.assistants.join(', ') }}
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="warning" size="small" @click="openEditCourseDialog(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteCourse(row.id)">删除</el-button>
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
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="学生" value="student" />
          </el-select>
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!userForm.id">
          <el-input v-model="userForm.password" type="password" />
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
        <el-form-item label="课程名" prop="name">
          <el-input v-model="courseForm.name" />
        </el-form-item>
        <el-form-item label="讲师" prop="instructor">
          <el-select
            v-model="courseForm.instructor"
            placeholder="选择讲师"
            filterable
            clearable
            multiple
            style="width: 100%"
            :filter-method="filterTeachers"
          >
            <el-option
              v-for="teacher in teachers"
              :key="teacher.email"
              :value="teacher.email"
            >
              <div class="teacher-option">
                <span class="teacher-name">{{ teacher.username }}</span>
                <span class="teacher-email">{{ teacher.email }}</span>
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
            :filter-method="filterAssistants"
          >
            <el-option
              v-for="assistant in assistants"
              :key="assistant.email"
              :value="assistant.email"
            >
              <div class="teacher-option">
                <span class="teacher-name">{{ assistant.username }}</span>
                <span class="teacher-email">{{ assistant.email }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="courseForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="courseDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCourse">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 用户管理相关
const activeTab = ref('users')
const userSearch = ref('')
const userDialogVisible = ref(false)
const userDialogTitle = ref('添加用户')
const userFormRef = ref(null)
const userForm = ref({
  id: null,
  username: '',
  email: '',
  role: '',
  password: ''
})
const userRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] }
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}
const users = ref([
  { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin' },
  { id: 2, username: 'teacher1', email: 'teacher1@example.com', role: 'teacher' },
  { id: 3, username: 'teacher1', email: 'teacher2@example.com', role: 'teacher' },
  { id: 4, username: 'student1', email: 'student1@example.com', role: 'student' }
])
const filteredUsers = computed(() => {
  return users.value.filter(user =>
    user.username.toLowerCase().includes(userSearch.value.toLowerCase())
  )
})

const openAddUserDialog = () => {
  userDialogTitle.value = '添加用户'
  userDialogVisible.value = true
}
const openEditUserDialog = (user) => {
  userDialogTitle.value = '编辑用户'
  userForm.value = { ...user, password: '' }
  userDialogVisible.value = true
}
const resetUserForm = () => {
  userForm.value = { id: null, username: '', email: '', role: '', password: '' }
  userFormRef.value?.resetFields()
}
const saveUser = () => {
  userFormRef.value.validate((valid) => {
    if (valid) {
      if (userForm.value.id) {
        const index = users.value.findIndex(u => u.id === userForm.value.id)
        users.value[index] = { ...userForm.value, password: undefined }
        ElMessage.success('用户更新成功')
      } else {
        users.value.push({
          id: users.value.length + 1,
          username: userForm.value.username,
          email: userForm.value.email,
          role: userForm.value.role
        })
        ElMessage.success('用户添加成功')
      }
      userDialogVisible.value = false
    }
  })
}
const deleteUser = (id) => {
  users.value = users.value.filter(user => user.id !== id)
  ElMessage.success('用户删除成功')
}
const filterUsers = () => {
  // 触发 computed 属性更新
}

// 课程管理相关
const courseSearch = ref('')
const courseDialogVisible = ref(false)
const courseDialogTitle = ref('添加课程')
const courseFormRef = ref(null)
const courseForm = ref({
  id: null,
  name: '',
  instructor: [],
  assistants: [],
  description: ''
})
const courseRules = {
  name: [{ required: true, message: '请输入课程名', trigger: 'blur' }],
  instructor: [{ required: true, type: 'array', min: 1, message: '请至少选择一名讲师', trigger: 'change' }],
  assistants: [{ required: true, type: 'array', min: 1, message: '请至少选择一名助教', trigger: 'change' }],
  description: [{ required: true, message: '请输入课程描述', trigger: 'blur' }]
}
const courses = ref([
  { id: 1, name: '数学基础', instructor: ['teacher1'], assistants: ['student1'], description: '基础数学课程' },
  { id: 2, name: '编程入门', instructor: ['teacher1'], assistants: ['student1'], description: 'Python编程入门' }
])
const filteredCourses = computed(() => {
  return courses.value.filter(course =>
    course.name.toLowerCase().includes(courseSearch.value.toLowerCase())
  )
})

const teachers = ref(users.value.filter(user => user.role === 'teacher'))
const assistants = ref(users.value.filter(user => user.role === 'student'))

const filterTeachers = (query) => {
  const lowerQuery = query.toLowerCase()
  teachers.value = users.value.filter(user => 
    user.role === 'teacher' && (
      user.username.toLowerCase().includes(lowerQuery) || 
      user.email.toLowerCase().includes(lowerQuery)
    )
  )
}

const filterAssistants = (query) => {
  const lowerQuery = query.toLowerCase()
  assistants.value = users.value.filter(user => 
    user.role === 'student' && (
      user.username.toLowerCase().includes(lowerQuery) || 
      user.email.toLowerCase().includes(lowerQuery)
    )
  )
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
  courseForm.value = { id: null, name: '', instructor: [], assistants: [], description: '' }
  courseFormRef.value?.resetFields()
  teachers.value = users.value.filter(user => user.role === 'teacher')
  assistants.value = users.value.filter(user => user.role === 'student')
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
          id: courses.value.length + 1,
          name: courseForm.value.name,
          instructor: courseForm.value.instructor,
          assistants: courseForm.value.assistants,
          description: courseForm.value.description
        })
        ElMessage.success('课程添加成功')
      }
      courseDialogVisible.value = false
    }
  })
}
const deleteCourse = (id) => {
  courses.value = courses.value.filter(course => course.id !== id)
  ElMessage.success('课程删除成功')
}
const filterCourses = () => {
  // 触发 computed 属性更新
}
</script>

<style scoped>
.admin-page {
  padding: 20px;
}
.action-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}
.teacher-option {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.teacher-name {
  flex: 1;
  text-align: left;
}
.teacher-email {
  flex: 1;
  text-align: right;
  color: #909399;
}
</style>