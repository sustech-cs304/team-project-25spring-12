<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="login-header">
        <img class="logo" src="../../assets/img/logo.svg" alt="Logo"/>
        <h1 class="login-title">后台管理系统</h1>
      </div>
      <el-form :model="param" :rules="rules" ref="login" size="large">
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="用户名" clearable>
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
              v-model="param.password"
              placeholder="密码"
              show-password
              clearable
              @keyup.enter="submitForm(login)"
          >
            <template #prepend>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <div class="login-options">
          <el-checkbox v-model="checked">记住密码</el-checkbox>
        </div>
        <el-button class="login-btn" type="primary" size="large" @click="submitForm(login)">登录</el-button>
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

interface LoginInfo {
  username: string;
  password: string;
}

const router = useRouter();
const checked = ref(localStorage.getItem('login-param') !== null);
const defParam = checked.value ? JSON.parse(localStorage.getItem('login-param')!) : null;

const param = reactive<LoginInfo>({
  username: defParam?.username || '',
  password: defParam?.password || '',
});

const rules: FormRules = {
  username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
  password: [{required: true, message: '请输入密码', trigger: 'blur'}],
};

const login = ref<FormInstance>();
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      ElMessage.success('登录成功');
      localStorage.setItem('vuems_name', param.username);
      router.push('/');
      checked.value
          ? localStorage.setItem('login-param', JSON.stringify(param))
          : localStorage.removeItem('login-param');
    } else {
      ElMessage.error('登录失败');
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

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0 20px;
  font-size: 14px;
}

.login-btn {
  width: 100%;
}

.login-footer-tip {
  margin-top: 15px;
  font-size: 12px;
  color: #999;
  text-align: center;
}

.login-footer-text {
  margin-top: 15px;
  font-size: 14px;
  text-align: center;
  color: #555;
}
</style>
