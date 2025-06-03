<template>
  <div class="widget-layout">
    <!-- 菜单 + 切换按钮区域 -->
    <div class="widget-menu-wrapper">
      <!-- 标题 -->
      <div class="menu-toggle">
        <el-button
            class="back-button"
            @click="goBackToCourse"
        >
          <el-icon>
            <ArrowLeft/>
          </el-icon>
          <span>返回</span>
        </el-button>
        <span class="menu-title">{{ title }}</span>
      </div>

      <!-- 菜单栏 -->
      <el-menu
          class="widget-menu"
          :default-active="activeWidgetId"
          mode="vertical"
          @select="handleMenuSelect"
      >
        <el-menu-item
            v-for="widget in widgetsSortedByIndex"
            :key="widget.id"
            :index="String(widget.id)"
            :style="getMenuItemStyle(widget)"
            class="hoverable-item"
        >
          <el-icon v-if="getIconComponent(widget)">
            <component :is="getIconComponent(widget)"/>
          </el-icon>
          <span>{{ widget.title }}</span>
        </el-menu-item>
      </el-menu>
      <el-popover
          :visible="showCreateWidgetPopover"
          placement="top"
          :width="180"
          v-if="editable"
      >
        <p>
          <el-select v-model="newWidgetType" placeholder="请选择类型">
            <el-option
                v-for="item in WidgetTypes"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </p>
        <div style="text-align:center; margin-top: 5px;">
          <el-button size="small" @click="showCreateWidgetPopover = false">取消</el-button>
          <el-button size="small" type="primary" @click="handleCreateWidget">确认</el-button>
        </div>
        <template #reference>
          <el-button @click="handleShowCreateWidgetPopover">
            <el-icon>
              <Plus/>
            </el-icon>
            <span>新建目录</span>
          </el-button>
        </template>
      </el-popover>
    </div>

    <!-- 内容区域 -->
    <div class="widget-content">
      <el-scrollbar class="widget-scroll-wrapper">
        <DynamicWidget
            v-if="activeWidget"
            :key="activeWidget.id"
            :data="activeWidget"
            :editable="editable"
            :ref="el => setWidgetRef(activeWidget.id, el)"
            @update="handleWidgetUpdate"
        />
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref, resolveComponent} from 'vue'
import type {Page} from "@/types/page"
import type {WidgetUnion} from '@/types/widgets'
import DynamicWidget from '@/views/widgets/dynamic-widget.vue'
import {getBodyColor, getHeaderColor, getWidgetStyle} from '@/utils/widgetColorIconManager'
import {createWidget, getPage} from "@/api/courseMaterial"
import {getRoleByCourseId} from "@/composables/useUserData";
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const WidgetTypes = [
    { value: 'notepdf', label: "互动式课件" },
    { value: 'doc', label: "文档" },
    { value: 'assignment', label: "作业" },
];

const route = useRoute()
const router = useRouter()

const goBackToCourse = () => {
  router.push({ name: 'course', params: { courseId: courseId.value } })
}

const activeWidgetId = ref<string>('')
const widgetRefs = new Map<string, any>()

const widgets = ref<WidgetUnion[]>([])
const title = ref('')

const pageId = ref<number>(-1)
const courseId = ref<number>(-1)
const role = ref<string>('')
const editable = computed(() => role.value === 'teaching assistant' || role.value === 'teacher')

onMounted(async () => {
  pageId.value = Number(route.params.pageId)
  const response = await getPage(pageId.value)
  const data = response.data as Page
  title.value = data.name
  widgets.value = data.widgets

  initActiveWidget()
  setTimeout(() => {
    widgetRefs.get(activeWidgetId.value)?.init?.()
  }, 50)

  courseId.value = Number(route.params.courseId)
  role.value = await getRoleByCourseId(courseId.value)
})

const widgetsSortedByIndex = computed(() => {
  return [...widgets.value].sort((a, b) => a.index - b.index)
})

const activeWidget = computed(() => {
  return widgets.value.find(w => w.id.toString() === activeWidgetId.value)
})

const getMenuItemStyle = (widget: WidgetUnion) => {
  const color = getWidgetStyle(widget.type).color
  return {
    backgroundColor: widget.id.toString() === activeWidgetId.value ? getHeaderColor(color) : getBodyColor(color),
    color: widget.id.toString() === activeWidgetId.value ? 'white' : 'black',
    fontWeight: 'bold',
    borderRadius: '6px',
    margin: '4px 8px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    justifyContent: 'flex-start',
    transition: 'all 0.2s',
  }
}

const getIconComponent = (widget: WidgetUnion) => {
  const iconName = getWidgetStyle(widget.type).icon
  return resolveComponent(iconName)
}

const setWidgetRef = (id: string, el: any) => {
  if (el) widgetRefs.set(id, el)
}

const initActiveWidget = () => {
  const widgetId = route.query.widget as string
  const matched = widgets.value.find(w => w.id.toString() === widgetId)
  if (matched) {
    activeWidgetId.value = matched.id.toString()
  } else if (widgets.value.length > 0) {
    const minWidget = widgetsSortedByIndex.value[0]
    activeWidgetId.value = minWidget.id.toString()
  }
}

const handleMenuSelect = (widgetId: number) => {
  activeWidgetId.value = widgetId.toString()
  setTimeout(() => {
    widgetRefs.get(widgetId.toString())?.init?.()
  }, 50)
}

const showCreateWidgetPopover = ref(false)
const newWidgetType = ref('')

const handleShowCreateWidgetPopover = () => {
  showCreateWidgetPopover.value = true
  newWidgetType.value = ''
}

const handleCreateWidget = async () => {
  showCreateWidgetPopover.value = false

  if (newWidgetType.value.length) {
    let newWidget: WidgetUnion = {
      index: widgets.value.length,
      type: newWidgetType.value,
      visible: true,
      page_id: pageId.value,
      title: WidgetTypes.find(item => item.value === newWidgetType.value)?.label,
    }
    switch (newWidgetType.value) {
      case "notepdf":
        break
      case "doc":
        break
      case "assignment":
        break
    }
    const response = await createWidget(newWidget)
    widgets.value.push(response.data)
  }
}

const handleWidgetUpdate = (data: WidgetUnion) => {
  const index = widgets.value.findIndex(w => w.id === data.id);
  if (index !== -1) {
    widgets.value.splice(index, 1, data);
  }
}
</script>

<style scoped>
.back-button {
  width: 90px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 16px;
  margin: 0;
  height: 100%;
  color: var(--el-color-primary);
}

.back-button span {
  margin-left: 8px;
}

.menu-toggle {
  height: 56px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
}

.widget-layout {
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.widget-menu {
  height: 100%;
}

.widget-menu-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-right: 1px solid #ebeef5;
  transition: width 0.3s ease-in-out;
  width: 300px;
  flex-shrink: 0;
}

.menu-title {
  font-weight: bold;
  font-size: 16px;
  transition: opacity 0.3s ease;
  white-space: nowrap;
  margin-left: 15px;
}

.hoverable-item:hover {
  filter: brightness(1.08);
  cursor: pointer;
}

.widget-content {
  flex: 1;
  height: 100%;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden;
}

.widget-scroll-wrapper {
  height: 100%;
  overflow: auto;
}
</style>