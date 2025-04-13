<template>
  <div class="error-page">
    <div class="error-box">
      <div class="error-code">401</div>
      <div class="error-desc">啊哦~ 你未登录或登录状态已过期</div>
      <div class="error-handle">
        <div class="countdown-text">{{ countdown }} 秒后返回登录页</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="401">
import {onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
const countdown = ref(3)

onMounted(() => {
  const interval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(interval)
      router.push('/login')
    }
  }, 1000)
})
</script>

<style scoped>
.error-page {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  background: #eef0fc;
  box-sizing: border-box;
}

.error-box {
  width: 400px;
  background-color: #fff;
  padding: 80px 50px;
  border-radius: 5px;
}

.error-code {
  line-height: 1;
  font-size: 100px;
  font-weight: bold;
  color: var(--el-color-primary);
  margin-bottom: 20px;
  text-align: center;
}

.error-desc {
  font-size: 20px;
  color: #777;
  text-align: center;
}

.error-handle {
  margin-top: 50px;
  text-align: center;
}

.countdown-text {
  font-size: 16px;
  color: #666;
}
</style>