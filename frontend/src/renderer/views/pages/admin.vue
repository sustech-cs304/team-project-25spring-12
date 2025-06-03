<template>
  <div class="admin-page">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 用户管理 -->
      <el-tab-pane label="用户管理" name="users">
        <div class="user-management">
          <div class="action-bar">
            <el-button type="primary" @click="openAddUserDialog">添加用户</el-button>
            <el-input
              v-model="usernameSearch"
              placeholder="搜索用户名"
              style="width: 200px; margin-right: 10px"
              clearable
              @input="filterUsers"
            />
            <el-input
              v-model="departmentSearch"
              placeholder="搜索部门"
              style="width: 200px; margin-right: 10px"
              clearable
              @input="filterUsers"
            />
            <el-input
              v-model="emailSearch"
              placeholder="搜索邮箱"
              style="width: 200px"
              clearable
              @input="filterUsers"
            />
          </div>
          <el-table
            :data="filteredUsers"
            style="width: 100%"
            border
            empty-text="请使用搜索框"
            @sort-change="handleUserSortChange"
          >
            <el-table-column prop="username" label="用户名" sortable />
            <el-table-column prop="name" label="姓名" sortable />
            <el-table-column prop="department" label="部门" sortable />
            <el-table-column prop="email" label="邮箱" sortable />
            <el-table-column prop="is_active" label="是否激活" sortable>
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">
                  {{ row.is_active ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_admin" label="是否管理员" sortable>
              <template #default="{ row }">
                <el-tag :type="row.is_admin ? 'success' : 'danger'">
                  {{ row.is_admin ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
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
            <el-select
              v-model="semesterFilter"
              style="width: 150px; margin-right: 10px"
              placeholder="选择学期"
              clearable
              @change="fetchCourses"
            >
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
            <el-table-column prop="course_code" label="课程代码" sortable />
            <el-table-column prop="name" label="课程名" sortable />
            <el-table-column prop="lecturer" label="讲师" sortable />
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
      <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="userDialogTitle === '编辑用户'" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="userForm.department" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="激活" prop="is_active">
          <el-switch v-model="userForm.is_active" active-text="是" inactive-text="否" />
        </el-form-item>
        <el-form-item label="管理员" prop="is_admin">
          <el-switch v-model="userForm.is_admin" active-text="是" inactive-text="否" />
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
          <el-select v-model="courseForm.semester_id" placeholder="选择学期">
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
            :filter-method="filterUsersForCourse"
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
            :filter-method="filterUsersForCourse"
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
            :filter-method="filterUsersForCourse"
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
          <el-date-picker
            v-model="semesterForm.start_time"
            type="date"
            placeholder="选择开始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="semesterForm.end_time"
            type="date"
            placeholder="选择结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
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
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import service from '../../utils/request';

// 用户管理相关
const activeTab = ref('users');
const usernameSearch = ref('');
const departmentSearch = ref('');
const emailSearch = ref('');
const userDialogVisible = ref(false);
const userDialogTitle = ref('添加用户');
const userFormRef = ref(null);
const userForm = ref({
  name: '',
  username: '',
  password: '',
  department: '',
  email: '',
  is_active: true,
  is_admin: false,
});
const userRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' },
  ],
  department: [{ required: true, message: '请输入部门', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] },
  ],
  is_active: [{ required: true, type: 'boolean', message: '请选择是否激活', trigger: 'change' }],
  is_admin: [{ required: true, type: 'boolean', message: '请选择是否管理员', trigger: 'change' }],
};
const filteredUsers = ref([]);

const filterUsers = async () => {
  try {
    if (!usernameSearch.value.trim() &&
        !departmentSearch.value.trim() &&
        !emailSearch.value.trim()) {
      filteredUsers.value = [];
      return;
    }
    const params = {};
    if (usernameSearch.value.trim())
      params.username = usernameSearch.value.trim();
    if (departmentSearch.value.trim())
      params.department = departmentSearch.value.trim();
    if (emailSearch.value.trim())
      params.email = emailSearch.value.trim();
    const response = await service.get('/user', { params });
    filteredUsers.value = response.data;
  } catch (error) {
    console.error('搜索用户失败:', error);
    ElMessage.error('搜索用户失败，请稍后重试');
    filteredUsers.value = [];
  }
};

const openAddUserDialog = () => {
  userDialogTitle.value = '添加用户';
  userDialogVisible.value = true;
};

const openEditUserDialog = (user) => {
  userDialogTitle.value = '编辑用户';
  userForm.value = {
    ...user,
    password: '', // 编辑时不回显密码
  };
  userDialogVisible.value = true;
};

const resetUserForm = () => {
  userForm.value = {
    name: '',
    username: '',
    password: '',
    department: '',
    email: '',
    is_active: true,
    is_admin: false,
  };
  userFormRef.value?.resetFields();
};

const saveUser = async () => {
  try {
    await userFormRef.value.validate(async (valid) => {
      if (!valid) return;
      const userData = {
        name: userForm.value.name,
        username: userForm.value.username,
        password: userForm.value.password,
        department: userForm.value.department,
        email: userForm.value.email,
        is_active: userForm.value.is_active,
        is_admin: userForm.value.is_admin,
      };
      if (userDialogTitle.value === '编辑用户') {
        // 编辑时仅发送非空密码
        if (!userData.password) delete userData.password;
        await service.put(`/users/${userForm.value.username}`, userData);
        const index = filteredUsers.value.findIndex((u) => u.username === userForm.value.username);
        if (index !== -1) {
          filteredUsers.value[index] = { ...userData };
        }
        ElMessage.success('用户更新成功');
      } else {
        const response = await service.post('/users', userData);
        filteredUsers.value.push(response.data);
        ElMessage.success('用户添加成功');
      }
      userDialogVisible.value = false;
    });
  } catch (error) {
    console.error('保存用户失败:', error);
    ElMessage.error('保存用户失败，请稍后重试');
  }
};

const deleteUser = (username) => {
  service
    .delete(`/users/${username}`)
    .then(() => {
      filteredUsers.value = filteredUsers.value.filter((user) => user.username !== username);
      ElMessage.success('用户删除成功');
    })
    .catch(() => {
      ElMessage.error('删除用户失败，请稍后重试');
    });
};

// 课程管理相关
const courseSearch = ref('');
const courseSearchType = ref('name');
const courseDialogVisible = ref(false);
const courseDialogTitle = ref('添加课程');
const courseFormRef = ref(null);
const courseForm = ref({
  id: null,
  semester_id: '',
  course_code: '',
  name: '',
  lecturer: '',
  assistants: [],
  students: [],
  location: '',
  time: '',
});
const courseRules = {
  semester_id: [{ required: true, message: '请选择学期', trigger: 'change' }],
  course_code: [{ required: true, message: '请输入课程代码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入课程名', trigger: 'blur' }],
  lecturer: [{ required: true, message: '请选择一名讲师', trigger: 'change' }],
  assistants: [{ required: false, type: 'array', trigger: 'change' }],
  students: [{ required: false, type: 'array', trigger: 'change' }],
  location: [{ required: false, message: '请输入课程地点', trigger: 'blur' }],
  time: [{ required: false, message: '请输入课程时间', trigger: 'blur' }],
};
const courses = ref([]);

const fetchCourses = async (semester_id) => {
  if (!semester_id) {
    courses.value = [];
    return;
  }
  try {
    const response = await service.get('/admin/semester/${semester_id}');
    const semesterCourses = response.data;
    const enrichedCourses = await Promise.all(
      semesterCourses.map(async (course) => {
        try {
          console.log('course:', course);
          const userResponse = await service.get('/class/${course.id}/user');
          const users = userResponse.data;
          const teacher = users.find((user) => user.role === 'teacher')?.username;
          const assistants = users
            .filter((user) => user.role === 'assistant')
            .map((user) => user.username);
          const students = users
            .filter((user) => user.role === 'student')
            .map((user) => user.username);
          return {
            id: course.id,
            course_code: course.courseCode,
            name: course.name,
            semester: course.semester,
            lecturer: course.lecturer,
            teacher,
            assistants,
            students,
            location: course.location,
            time: course.time,
          };
        } catch (error) {
          console.error('获取课程 ${course.id} 的用户数据失败:', error);
          return {
            id: course.id,
            course_code: course.courseCode,
            name: course.name,
            semester: course.semester,
            lecturer: course.lecturer,
            teacher: '',
            assistants: [],
            students: [],
            location: course.location,
            time: course.time,
          };
        }
      })
    );
    courses.value = enrichedCourses;
    console.log('Enriched Courses:', courses.value);
    ElMessage.success('已加载学期内课程信息');
  } catch (error) {
    console.error('获取课程数据失败:', error);
    ElMessage.error('加载学期详细信息失败，请稍后重试');
    courses.value = [];
  }
};

const filteredCourses = computed(() => {
  return courses.value.filter((course) => {
    const matchesSearch =
      courseSearchType.value === 'course_code'
        ? course.course_code.toLowerCase().includes(courseSearch.value.toLowerCase())
        : course.name.toLowerCase().includes(courseSearch.value.toLowerCase());
    return matchesSearch;
  });
});

const filteredUsersForCourse = ref([]);

const filterUsersForCourse = async (query) => {
  try {
    if (!query.trim()) {
      filteredUsersForCourse.value = [];
      return;
    }
    const response = await service.get('/admin/user', {
      params: {
        name: query.trim(),
      },
    });
    filteredUsersForCourse.value = response.data;
  } catch (error) {
    console.error('搜索用户失败:', error);
    ElMessage.error('搜索用户失败，请稍后重试');
    filteredUsersForCourse.value = [];
  }
};

const openAddCourseDialog = () => {
  courseDialogTitle.value = '添加课程';
  courseDialogVisible.value = true;
};

const openEditCourseDialog = (course) => {
  courseDialogTitle.value = '编辑课程';
  courseForm.value = { ...course };
  courseDialogVisible.value = true;
};

const resetCourseForm = () => {
  courseForm.value = {
    id: null,
    semester_id: '',
    course_code: '',
    name: '',
    lecturer: '',
    assistants: [],
    students: [],
    location: '',
    time: '',
  };
  courseFormRef.value?.resetFields();
  filteredUsersForCourse.value = [];
};

const saveCourse = async () => {
  try {
    await courseFormRef.value.validate(async (valid) => {
      if (!valid) return;
      const courseData = {
        semester_id: courseForm.value.semester_id,
        course_code: courseForm.value.course_code,
        name: courseForm.value.name,
        location: courseForm.value.location,
        time: courseForm.value.time,
      };
      let courseId = courseForm.value.id;
      if (courseId) {
        await service.patch(`/class/${courseId}`, courseData);
        const userResponse = await service.get(`/class/${courseId}/user`);
        const existingUsers = userResponse.data;
        const existingUsersByRole = {
          teacher: existingUsers.filter((u) => u.role === 'teacher').map((u) => u.username),
          assistant: existingUsers.filter((u) => u.role === 'assistant').map((u) => u.username),
          student: existingUsers.filter((u) => u.role === 'student').map((u) => u.username),
        };
        const newUsers = [
          { username: courseForm.value.lecturer, role: 'teacher' },
          ...courseForm.value.assistants.map((username) => ({ username, role: 'assistant' })),
          ...courseForm.value.students.map((username) => ({ username, role: 'student' })),
        ];
        const newUsersByRole = {
          teacher: newUsers.filter((u) => u.role === 'teacher').map((u) => u.username).filter(Boolean),
          assistant: newUsers.filter((u) => u.role === 'assistant').map((u) => u.username),
          student: newUsers.filter((u) => u.role === 'student').map((u) => u.username),
        };
        for (const role of ['teacher', 'assistant', 'student']) {
          const usersToAdd = newUsersByRole[role].filter(
            (username) => !existingUsersByRole[role].includes(username)
          );
          if (usersToAdd.length > 0) {
            await service.post(`/class/user`, {
              class_id: courseId,
              usernames: usersToAdd,
              role,
            });
          }
        }
        for (const role of ['teacher', 'assistant', 'student']) {
          const usersToRemove = existingUsersByRole[role].filter(
            (username) => !newUsersByRole[role].includes(username)
          );
          for (const username of usersToRemove) {
            await service.delete(`/class/${courseId}/user/${username}`);
          }
        }
        const index = courses.value.findIndex((c) => c.id === courseId);
        if (index !== -1) {
          courses.value[index] = {
            ...courses.value[index],
            ...courseData,
            lecturer: courseForm.value.lecturer,
            assistants: courseForm.value.assistants,
            students: courseForm.value.students,
          };
        }
        ElMessage.success('课程更新成功');
      } else {
        const response = await service.post('/class', courseData);
        courseId = response.data.id;
        const newUsers = [
          { username: courseForm.value.lecturer, role: 'teacher' },
          ...courseForm.value.assistants.map((username) => ({ username, role: 'assistant' })),
          ...courseForm.value.students.map((username) => ({ username, role: 'student' })),
        ].filter((u) => u.username);
        const usersByRole = {
          teacher: newUsers.filter((u) => u.role === 'teacher').map((u) => u.username),
          assistant: newUsers.filter((u) => u.role === 'assistant').map((u) => u.username),
          student: newUsers.filter((u) => u.role === 'student').map((u) => u.username),
        };
        for (const role of ['teacher', 'assistant', 'student']) {
          if (usersByRole[role].length > 0) {
            await service.post(`/class/user`, {
              class_id: courseId,
              usernames: usersByRole[role],
              role,
            });
          }
        }
        courses.value.push({
          ...courseData,
          id: courseId,
          lecturer: courseForm.value.lecturer,
          assistants: courseForm.value.assistants,
          students: courseForm.value.students,
        });
        ElMessage.success('课程添加成功');
      }
      courseDialogVisible.value = false;
    });
  } catch (error) {
    console.error('保存课程失败:', error);
    ElMessage.error('保存课程失败，请稍后重试');
  }
};

const deleteCourse = (id) => {
  service
    .delete(`/class/${id}`)
    .then(() => {
      courses.value = courses.value.filter((course) => course.id !== id);
      ElMessage.success('课程删除成功');
    })
    .catch(() => {
      ElMessage.error('删除课程失败，请稍后重试');
    });
};

const filterCourses = () => {};

// 学期管理相关
const semesterSearch = ref('');
const semesterDialogVisible = ref(false);
const semesterDialogTitle = ref('添加学期');
const semesterFormRef = ref(null);
const semesterForm = ref({
  id: null,
  name: '',
  start_time: '',
  end_time: '',
});
const semesters = ref([
  { id: 1, name: '2023 春季', start_time: '2023-02-01', end_time: '2023-06-30' },
  { id: 2, name: '2023 秋季', start_time: '2023-09-01', end_time: '2024-01-31' },
  { id: 3, name: '2024 春季', start_time: '2024-02-01', end_time: '2024-06-30' },
  { id: 4, name: '2024 秋季', start_time: '2024-09-01', end_time: '2025-01-31' },
  { id: 5, name: '2025 春季', start_time: '2025-02-01', end_time: '2025-06-30' },
]);

const fetchSemesters = async () => {
  try {
    const response = await service.get('/class/semester');
    semesters.value = response.data;
    console.log('Loaded semesters:', semesters.value);
    ElMessage.success('学期数据加载成功');
  } catch (error) {
    ElMessage.error('加载学期数据失败，请稍后重试');
    console.error('Error fetching semesters:', error);
  }
};

const semesterFilter = ref('');

const invertedSemesters = computed(() => {
  return [...semesters.value].sort((a, b) => b.id - a.id);
});

const semesterRules = {
  name: [{ required: true, message: '请输入学期名称', trigger: 'blur' }],
  start_time: [
    { required: true, message: '请选择开始日期', trigger: 'change' },
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请选择开始日期'));
        } else if (semesterForm.value.end_time && value > semesterForm.value.end_time) {
          callback(new Error('开始日期不能晚于结束日期'));
        } else {
          callback();
        }
      },
      trigger: 'change',
    },
  ],
  end_time: [
    { required: true, message: '请选择结束日期', trigger: 'change' },
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请选择结束日期'));
        } else if (semesterForm.value.start_time && value < semesterForm.value.start_time) {
          callback(new Error('结束日期不能早于开始日期'));
        } else {
          callback();
        }
      },
      trigger: 'change',
    },
  ],
};

const filteredSemesters = computed(() => {
  return semesters.value.filter((semester) =>
    semester.name.toLowerCase().includes(semesterSearch.value.toLowerCase())
  );
});

const openAddSemesterDialog = () => {
  semesterDialogTitle.value = '添加学期';
  semesterDialogVisible.value = true;
};

const openEditSemesterDialog = (semester) => {
  semesterDialogTitle.value = '编辑学期';
  semesterForm.value = { ...semester };
  semesterDialogVisible.value = true;
};

const resetSemesterForm = () => {
  semesterForm.value = { id: null, name: '', start_time: '', end_time: '' };
  semesterFormRef.value?.resetFields();
};

const saveSemester = async () => {
  try {
    await semesterFormRef.value.validate(async (valid) => {
      if (!valid) return;
      const semesterData = {
        name: semesterForm.value.name,
        start_time: semesterForm.value.start_time,
        end_time: semesterForm.value.end_time,
      };
      if (semesterForm.value.id) {
        await service.patch(`/class/semester/${semesterForm.value.id}`, semesterData);
        const index = semesters.value.findIndex((s) => s.id === semesterForm.value.id);
        if (index !== -1) {
          semesters.value[index] = { ...semesterForm.value };
        }
        ElMessage.success('学期更新成功');
      } else {
        const response = await service.post('/class/semester', semesterData);
        console.log('New Semester Res: ', response);
        const newSemester = {
          id: response.data.id,
          ...semesterData,
        };
        console.log('New Semester: ', newSemester);
        semesters.value.push(newSemester);
        ElMessage.success('学期添加成功');
      }
      semesterDialogVisible.value = false;
    });
  } catch (error) {
    console.error('保存学期失败:', error);
    ElMessage.error('保存学期失败，请稍后重试');
  }
};

const deleteSemester = (id) => {
  const isUsed = courses.value.some((course) => course.semester === id);
  if (isUsed) {
    ElMessage.error('无法删除正在被课程使用的学期');
    return;
  }
  service
    .delete(`/class/semester/${id}`)
    .then(() => {
      semesters.value = semesters.value.filter((semester) => semester.id !== id);
      ElMessage.success('学期删除成功');
    })
    .catch(() => {
      ElMessage.error('删除学期失败，请稍后重试');
    });
};

const filterSemesters = () => {};

onMounted(fetchSemesters);
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