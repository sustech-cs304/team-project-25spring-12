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

        <!-- 消息通知 -->
        <el-tooltip effect="dark" content="消息" placement="bottom">
          <div class="btn-icon" @click="goToMessages">
            <el-icon>
              <Bell/>
            </el-icon>
            <span v-if="unreadCount > 0" class="btn-bell-badge"></span>
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
              <el-dropdown-item command="settings">
                <el-icon>
                  <Setting/>
                </el-icon>
                设置
              </el-dropdown-item>
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
import {ref, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import {
  HomeFilled,
  ChatRound,
  FullScreen,
  Bell,
  ArrowDown,
  Link,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue';

// 用户数据
const username = ref(localStorage.getItem('vuems_name') || '用户');
const userAvatar = ref('../assets/img/img.jpg'); // TODO: 从用户信息获取头像
const unreadCount = ref(1); // TODO: 从API获取未读消息数

// 路由和状态管理
const router = useRouter();

// 导航功能
const goToHome = () => {
  router.push('/')
};

const goToArguePost = () => {
  // TODO: 跳转到反馈页面
  // router.push('/feedback');
};

const goToMessages = () => {
  router.push('/messages');
};

// 用户菜单操作
const handleCommand = (command: string) => {
  if (command === 'logout') {
    // TODO: 登出逻辑
    // localStorage.removeItem('vuems_name');
    // router.push('/login');
  } else if (command === 'settings') {
    // TODO: 跳转到设置页面
    // router.push('/settings');
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

.btn-bell-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #f56c6c;
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