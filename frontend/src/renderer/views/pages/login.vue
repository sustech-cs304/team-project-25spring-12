<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="login-header">
        <img class="logo" src="../../assets/img/logo.svg" alt="Logo"/>
        <h1 class="login-title">后台管理系统</h1>
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
import {reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import type {FormInstance, FormRules} from 'element-plus';
import {ElMessage} from 'element-plus';
import {useTabsStore} from '@/store/tabs';
import {useUserStore} from '@/store/user';
import {useLogin} from "@/composables/useLogin";
import {LoginRequest} from "@/types/auth";
import request from "@/utils/request";
import { assert } from 'pdfjs-dist/types/src/shared/util';

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
        const resp = await request.get(`/user/${loginFormData.username}`);
        console.log(resp.data);
        if (!resp.data.isActive) {
          throw new Error('Inactive');
        }
        userStore.setAdmin(resp.data.isAdmin);
        ElMessage.success('登录成功');
        await router.push('/');
      } catch (error) {
        const status = error?.response?.status;
        if (status === 401) {
          ElMessage.error('登录失败，请检查用户名或密码');
        }
        if ((<Error>error).message === 'Inactive') {
          ElMessage.error('账号未激活，请联系管理员');
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
  width: 420px;
  padding: 40px 50px;
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
</style>
