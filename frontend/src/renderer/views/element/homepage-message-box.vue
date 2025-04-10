<template>
  <el-scrollbar height="150px" always>
    <el-table :data="sortedNotifications" :show-header="false" style="width: 100%">
      <el-table-column>
        <template #default="scope">
          <span
              class="message-title"
              :class="{ read: scope.row.read }"
              @click="() => handleClick(scope.row)"
          >
            {{ scope.row.title }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="date" width="180"></el-table-column>
      <el-table-column width="120">
        <template #default="scope">
          <el-button
              size="small"
              @click="handleRead(scope.row)"
              :disabled="scope.row.read"
          >
            标为已读
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-scrollbar>

  <div class="handle-row" style="margin-top: 20px">
    <el-button type="primary" @click="handleAllRead">全部标为已读</el-button>
  </div>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue';

interface Notification {
  date: string;
  title: string;
  link: string;
  read: boolean;
}

const notifications = ref<Notification[]>([
  {
    date: '2025-04-10 16:00:00',
    title: '4 点的通知',
    link: '',
    read: false,
  },
  {
    date: '2025-04-10 18:00:00',
    title: '6 点的通知',
    link: '',
    read: false,
  },
  {
    date: '2025-04-10 20:00:00',
    title: '8 点的通知',
    link: '',
    read: true,
  },
  {
    date: '2025-03-31 18:00:00',
    title: '上个月的通知',
    link: '',
    read: false,
  },
  {
    date: '2025-04-10 22:00:00',
    title: '10 点的通知',
    link: '',
    read: false,
  }
]);

const sortedNotifications = computed(() => {
  return [...notifications.value].sort((a, b) => {
    if (a.read !== b.read) {
      return a.read ? 1 : -1; // 未读排前
    }
    return new Date(b.date).getTime() - new Date(a.date).getTime(); // 时间新排前
  });
});

const handleRead = (item: Notification) => {
  item.read = true;
};

const handleAllRead = () => {
  notifications.value.forEach(n => (n.read = true));
};

const handleClick = (item: Notification) => {
  console.log('click')
  // TODO
};
</script>

<style scoped>
.message-title {
  cursor: pointer;
  color: var(--el-color-primary);
  font-weight: bold;
}

.message-title.read {
  color: #999;
  font-weight: normal;
}
</style>