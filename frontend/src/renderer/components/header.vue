<template>
  <div class="header">
    <!-- 左侧区域 -->
    <div class="header-left">
      <img class="logo" src="../assets/img/logo.svg" alt="Logo"/>
      <div class="web-title">后台管理系统</div>

      <!-- 导航按钮 -->
      <div class="nav-buttons">
        <el-tooltip effect="dark" content="首页" placement="bottom">
          <div class="btn-icon" @click="goToHome">
            <el-icon>
              <HomeFilled/>
            </el-icon>
          </div>
        </el-tooltip>

        <el-tooltip effect="dark" content="反馈" placement="bottom">
          <div class="btn-icon" @click="goToArguePost">
            <el-icon>
              <ChatRound/>
            </el-icon>
          </div>
        </el-tooltip>
      </div>
    </div>

    <!-- 右侧区域 -->
    <div class="header-right">
      <div class="header-user-con">
        <!-- 全屏按钮 -->
        <el-tooltip effect="dark" content="全屏" placement="bottom">
          <div class="btn-icon" @click="setFullScreen">
            <el-icon>
              <FullScreen/>
            </el-icon>
          </div>
        </el-tooltip>

        <!-- 用户信息 -->
        <el-avatar class="user-avatar" :size="30" :src="userAvatar"/>
        <el-dropdown class="user-name" trigger="click" @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{ username }}
                        <el-icon class="el-icon--right">
                            <arrow-down/>
                        </el-icon>
                    </span>
          <template #dropdown>
            <el-dropdown-menu>
              <a href="https://github.com/sustech-cs304/team-project-25spring-12" target="_blank">
                <el-dropdown-item>
                  <el-icon>
                    <Link/>
                  </el-icon>
                  项目仓库
                </el-dropdown-item>
              </a>
              <el-dropdown-item divided command="logout">
                <el-icon>
                  <SwitchButton/>
                </el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import {
  HomeFilled,
  ChatRound,
  FullScreen,
  Bell,
  ArrowDown,
  Link,
  SwitchButton
} from '@element-plus/icons-vue';
import {useUserStore} from "@/store/user";

const userStore = useUserStore()
const router = useRouter()

const username = ref(userStore.username);
const userAvatar = ref('../assets/img/img.jpg');

const goToHome = () => {
  router.push('/homepage')
};

const goToArguePost = () => {
  // TODO: 跳转到反馈页面
  // router.push('/feedback');
};

const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.clearToken()
    router.push('/login')
  }
};

// 全屏功能
const setFullScreen = () => {
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    document.body.requestFullscreen();
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  color: var(--header-text-color);
  background-color: var(--header-bg-color);
  border-bottom: 1px solid var(--border-color);
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
  height: 100%;
}

.logo {
  width: 35px;
  height: 35px;
}

.web-title {
  font-size: 22px;
  font-weight: 600;
}

.nav-buttons {
  display: flex;
  gap: 10px;
  margin-left: 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-user-con {
  display: flex;
  align-items: center;
  gap: 15px;
  height: 100%;
}

.btn-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--header-text-color);
}

.btn-icon:hover {
  background-color: var(--hover-bg-color);
  transform: scale(1.05);
}

.user-avatar {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.user-avatar:hover {
  transform: scale(1.1);
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  color: var(--header-text-color);
  cursor: pointer;
  font-size: 14px;
  gap: 4px;
}

.el-dropdown-menu__item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
}
</style>