<template>
  <div class="main-container" ref="calendarWrapper">
    <FullCalendar
        :options="calendarOptions"
        ref="calendar"
        class="fc-theme-standard"
    />
  </div>

  <!-- 作业详情抽屉 -->
  <el-drawer
      v-model="drawerVisible"
      title="作业详情"
      size="400px"
      direction="rtl"
  >
    <template v-if="selectedDeadline">
      <p><strong>作业名称：</strong>{{ selectedDeadline.widgetTitle }}</p>
      <p><strong>所属课程：</strong>{{ selectedDeadline.courseCode }} {{ selectedDeadline.className }}</p>
      <p><strong>教学章节：</strong>{{ selectedDeadline.pageName }}</p>
      <p><strong>截止时间：</strong>{{ selectedDeadline.ddl }}</p>
    </template>

    <template #footer>
      <div style="text-align: right">
        <el-button type="primary" @click="goToTask">前往完成</el-button>
        <el-button type="danger" @click="dismissReminder">不再提醒</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

interface Deadline {
  widgetId: string
  widgetTitle: string
  pageId: string
  pageName: string
  ddl: string
  classId: string
  courseCode: string
  className: string
}

const deadlines = ref<Deadline[]>([
  {
    widgetId: 'w1',
    widgetTitle: '练习1.5',
    pageId: 'p1',
    pageName: '第一节 第二课',
    ddl: '2025-04-15',
    classId: 'c1',
    courseCode: 'CS101',
    className: '计算机导论'
  },
  {
    widgetId: 'w2',
    widgetTitle: '项目报告',
    pageId: 'p2',
    pageName: '第五节 第三课',
    ddl: '2025-04-18',
    classId: 'c1',
    courseCode: 'CS101',
    className: '计算机导论'
  }
])

const drawerVisible = ref(false)
const selectedDeadline = ref<Deadline | null>(null)
const calendar = ref()
const calendarWrapper = ref()

const calendarOptions = {
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  height: '100%',
  events: deadlines.value.map(item => ({
    title: item.widgetTitle,
    start: item.ddl,
    extendedProps: item
  })),
  eventClick(info: any) {
    selectedDeadline.value = info.event.extendedProps
    drawerVisible.value = true
  },
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  }
}

// ⏱ ResizeObserver 监听容器变化并刷新 FullCalendar
let resizeObserver: ResizeObserver

onMounted(() => {
  if (calendarWrapper.value) {
    resizeObserver = new ResizeObserver(() => {
      if (calendar.value) {
        calendar.value.getApi().updateSize()
      }
    })
    resizeObserver.observe(calendarWrapper.value)
  }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
})

const goToTask = () => {
  // TODO: 前往完成
}

const dismissReminder = () => {
  // TODO: 不再提醒
}
</script>

<style scoped>
.main-container {
  height: calc(100vh - 250px);
  min-height: 400px;
  overflow: hidden;
}
</style>
