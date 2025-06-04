<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="login-header">
        <img class="logo" src="../../assets/img/logo.svg" alt="Logo" />
        <h1 class="login-title">
          <template v-for="(char, index) in typedChars" :key="index">
            <span
                :class="getCharClass(char)"
                v-text="char"
            />
          </template>
          <span class="cursor">|</span>
        </h1>
      </div>
      <el-form :model="loginFormData" :rules="rules" ref="loginForm" size="large">
        <el-form-item prop="username">
          <el-input v-model="loginFormData.username" placeholder="用户名" clearable>
            <template #prepend>
              <el-icon>
                <User/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              type="password"
              v-model="loginFormData.password"
              placeholder="密码"
              show-password
              clearable
              @keyup.enter="submitForm()"
          >
            <template #prepend>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-button class="login-btn" type="primary" size="large" @click="submitForm()">登录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import {reactive, ref, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import type {FormInstance, FormRules} from 'element-plus';
import {ElMessage} from 'element-plus';
import {useTabsStore} from '@/store/tabs';
import {useUserStore} from '@/store/user';
import {useLogin} from "@/composables/useLogin";
import {LoginRequest} from "@/types/auth";

// 文本内容（可调）
const fullText = 'Ave MujiClass 课程信息系统'
const typedChars = ref<string[]>([])

onMounted(() => {
  let i = 0
  const interval = setInterval(() => {
    typedChars.value.push(fullText[i])
    i++
    if (i >= fullText.length) clearInterval(interval)
  }, 60)
})

// 区分字符类型（英文、中文、空格）
function getCharClass(char: string) {
  if (char === ' ') return 'space'
  if (/[A-Za-z]/.test(char)) return 'brand-en'
  if (/[\u4e00-\u9fa5]/.test(char)) return 'brand-cn'
  return ''
}

const router = useRouter();
const userStore = useUserStore();

const rules: FormRules = {
  username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
  password: [{required: true, message: '请输入密码', trigger: 'blur'}],
};

const {login} = useLogin();
const loginForm = ref<FormInstance>();
const loginFormData = reactive<LoginRequest>({
  username: '',
  password: '',
});

const submitForm = () => {
  if (!loginForm.value) return;

  loginForm.value.validate(async (valid) => {
    if (valid) {
      try {
        const result = await login(loginFormData);
        userStore.setToken(result.accessToken);
        userStore.setUsername(loginFormData.username);
        ElMessage.success('登录成功');
        await router.push('/');
      } catch (error) {
        const status = error?.response?.status;
        if (status === 401) {
          ElMessage.error('登录失败，请检查用户名或密码');
        }
      }
    }
  });
};

useTabsStore().clearTabs();
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f6f9fc;
}

.login-container {
  width: 540px;
  padding: 40px 100px;
  background-color: white;
  border-radius: 8px;
  box-sizing: border-box;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.login-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
}

.logo {
  width: 32px;
  height: 32px;
  margin-right: 10px;
}

.login-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e40af;
}

.login-btn {
  width: 100%;
}

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600&family=Noto+Serif+SC:wght@500&display=swap');

.login-header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 30px;
  white-space: nowrap;
}

.logo {
  width: 60px;
  height: 60px;
  margin-right: 16px;
  transition: margin 0.3s ease;
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  display: flex;
  align-items: center;
  font-family: 'Montserrat', 'Noto Serif SC', sans-serif;
}

/* 字体样式 */
.brand-en {
  font-family: 'Montserrat', sans-serif;
  background: linear-gradient(90deg, #2563eb, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-cn {
  font-family: 'Noto Serif SC', serif;
  color: #374151;
}

.space {
  display: inline-block;
  width: 0.5em;
}

/* 光标动画 */
.cursor {
  font-weight: 400;
  margin-left: 2px;
  color: rgba(0, 0, 0, 0.2);
  animation: blink-caret 0.75s step-end infinite;
}

@keyframes blink-caret {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

</style>
