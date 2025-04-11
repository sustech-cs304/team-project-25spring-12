<template>
  <div class="main-container" ref="calendarWrapper">
    <FullCalendar
        :options="calendarOptions"
        ref="calendar"
        class="custom-calendar-theme"
    />
  </div>

  <!-- 作业详情抽屉 -->
  <el-drawer
      v-model="drawerVisible"
      title="作业详情"
      size="400px"
      direction="rtl"
      class="assignment-drawer"
      :show-close="false"
      @open="onDrawerOpen"
  >
    <template v-if="selectedDeadline">
      <div class="drawer-header">
        <h3 class="assignment-title">
          <el-icon><Notebook /></el-icon>
          {{ selectedDeadline.widgetTitle }}
        </h3>
        <div class="deadline-countdown" :class="getCountdownClass(selectedDeadline.ddl)">
          <el-icon><Clock /></el-icon>
          剩余 {{ calculateDaysLeft(selectedDeadline.ddl) }} 天
        </div>
      </div>

      <el-divider />

      <div class="assignment-details">
        <div class="detail-item">
          <el-icon><Collection /></el-icon>
          <div>
            <div class="detail-label">所属课程</div>
            <div class="detail-value">{{ selectedDeadline.courseCode }} {{ selectedDeadline.className }}</div>
          </div>
        </div>

        <div class="detail-item">
          <el-icon><Document /></el-icon>
          <div>
            <div class="detail-label">教学章节</div>
            <div class="detail-value">{{ selectedDeadline.pageName }}</div>
          </div>
        </div>

        <div class="detail-item">
          <el-icon><AlarmClock /></el-icon>
          <div>
            <div class="detail-label">截止时间</div>
            <div class="detail-value highlight">{{ formatDateTime(selectedDeadline.ddl) }}</div>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <div class="drawer-footer">
        <el-button
            type="primary"
            @click="goToTask"
            size="large"
            class="action-button"
        >
          <el-icon><Link /></el-icon>
          前往完成
        </el-button>
        <el-button
            type="danger"
            @click="dismissReminder"
            size="large"
            class="action-button"
            plain
        >
          <el-icon><BellFilled /></el-icon>
          不再提醒
        </el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import { Notebook, Clock, Collection, Document, AlarmClock, Link, BellFilled } from '@element-plus/icons-vue'

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
    ddl: '2025-04-12',
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
  },
  {
    widgetId: 'w2',
    widgetTitle: '项目报告',
    pageId: 'p2',
    pageName: '第五节 第三课',
    ddl: '2025-04-28',
    classId: 'c1',
    courseCode: 'MATH101',
    className: '计算机导论'
  }
])

const drawerVisible = ref(false)
const selectedDeadline = ref<Deadline | null>(null)
const calendar = ref()
const calendarWrapper = ref()

/*
* AI generated
* 这段代码由 DeepSeek 生成，我要求它使用哈希算法，用courseCode动态生成一个颜色
* 来美化 DDL 日历的表现。
* */

// 替换原来的 getEventColor 函数
function getEventColor(courseCode: string): string {
  // 哈希函数 - 将字符串转换为哈希值
  const hash = stringToHash(courseCode)

  // 使用哈希值生成HSL颜色
  const hue = hash % 360  // 色调 (0-359)
  const saturation = 70 + (hash % 15)  // 饱和度 (70-85%)
  const lightness = 50 + (hash % 10)  // 明度 (50-60%)

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`
}

// 辅助函数：将字符串转换为稳定的哈希值
function stringToHash(str: string): number {
  let hash = 0
  if (str.length === 0) return hash

  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // 转换为32位整数
  }

  return Math.abs(hash)
}

// 辅助函数：根据背景色决定文字颜色（确保可读性）
function getTextColor(bgColor: string): string {
  // 如果是HSL颜色，提取亮度值
  if (bgColor.startsWith('hsl')) {
    const lightnessMatch = bgColor.match(/[\d.]+(?=%\))/)
    if (lightnessMatch) {
      const lightness = parseFloat(lightnessMatch[0])
      return lightness > 60 ? '#333' : '#fff'
    }
  }
  return '#fff' // 默认返回白色文字
}

const calendarOptions = {
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  height: '100%',
  events: deadlines.value.map(item => ({
    title: `${item.courseCode}`,
    start: item.ddl,
    extendedProps: item,
    backgroundColor: getEventColor(item.courseCode),
    borderColor: getEventColor(item.courseCode),
    textColor: getTextColor(getEventColor(item.courseCode)),
    className: 'calendar-event'
  })),
  eventClick(info: any) {
    selectedDeadline.value = info.event.extendedProps
    drawerVisible.value = true
  },
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: ''
  },
  dayHeaderClassNames: 'calendar-day-header',
  dayCellClassNames: 'calendar-day-cell',
  nowIndicator: true,
  eventMouseEnter(info: any) {
    info.el.style.transform = 'scale(1.02)'
    info.el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)'
  },
  eventMouseLeave(info: any) {
    info.el.style.transform = ''
    info.el.style.boxShadow = ''
  }
}

function calculateDaysLeft(ddl: string): number {
  const today = new Date()
  const deadline = new Date(ddl)
  const diffTime = deadline.getTime() - today.getTime()
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

function getCountdownClass(ddl: string): string {
  const daysLeft = calculateDaysLeft(ddl)
  if (daysLeft <= 3) return 'urgent'
  if (daysLeft <= 7) return 'warning'
  return 'normal'
}

function formatDateTime(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

const goToTask = () => {
  // TODO: 前往完成
}

const dismissReminder = () => {
  // TODO: 不再提醒
}

const onDrawerOpen = () => {}

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
</script>

<style scoped>
.main-container {
  height: calc(100vh - 250px);
  min-height: 400px;
  overflow: hidden;
}

.assignment-drawer {
  --el-drawer-padding-primary: 20px;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.assignment-title {
  margin: 0;
  font-size: 18px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.deadline-countdown {
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.deadline-countdown.normal {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.deadline-countdown.warning {
  background-color: #fff8e1;
  color: #ff8f00;
}

.deadline-countdown.urgent {
  background-color: #ffebee;
  color: #c62828;
}

.assignment-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.detail-item .el-icon {
  font-size: 20px;
  color: #409eff;
  margin-top: 2px;
}

.detail-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}

.detail-value {
  font-size: 15px;
  color: #606266;
}

.highlight {
  color: #e74c3c;
  font-weight: 500;
}

.drawer-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

.action-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.custom-calendar-theme {
  --fc-border-color: #ebeef5;
  --fc-page-bg-color: #ffffff;
  --fc-today-bg-color: rgba(52, 152, 219, 0.1);
  --fc-neutral-bg-color: #f5f7fa;
  --fc-highlight-color: rgba(52, 152, 219, 0.2);
}

.custom-calendar-theme .fc-toolbar-title {
  font-size: 1.4em;
  color: #303133;
  font-weight: 600;
}

.custom-calendar-theme .calendar-day-header {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 500;
  padding: 8px 0;
}

.custom-calendar-theme .calendar-day-cell {
  transition: background-color 0.2s;
}

.custom-calendar-theme .calendar-day-cell:hover {
  background-color: #f0f2f5;
}

.custom-calendar-theme .fc-day-today {
  background-color: rgba(52, 152, 219, 0.1) !important;
}

.custom-calendar-theme .fc-day-today .fc-daygrid-day-number {
  color: #3498db;
  font-weight: bold;
}

.custom-calendar-theme .calendar-event {
  transition: all 0.2s ease;
  cursor: pointer;
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 0.9em;
}

.custom-calendar-theme .fc-button {
  transition: all 0.2s;
}

.custom-calendar-theme .fc-button:hover {
  transform: translateY(-1px);
}

.custom-calendar-theme .fc-button-primary {
  background-color: #3498db;
  border-color: #3498db;
}

.custom-calendar-theme .fc-button-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.custom-calendar-theme .fc-button-primary:not(:disabled).fc-button-active {
  background-color: #2980b9;
  border-color: #2980b9;
}
</style>