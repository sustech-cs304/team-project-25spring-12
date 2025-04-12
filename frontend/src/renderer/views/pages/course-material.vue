<template>
  <div class="widget-layout">
    <el-menu
        class="widget-menu"
        :default-active="activeWidgetId"
        :collapse="collapsed"
        @select="handleMenuSelect"
        :collapse-transition="true"
        mode="vertical"
    >
      <el-menu-item index="__toggle" @click="toggleCollapse" style="cursor: pointer;">
        <el-icon>
          <component :is="collapsed ? 'ArrowRightBold' : 'ArrowLeftBold'" />
        </el-icon>
        <span v-if="!collapsed">{{ title }}</span>
      </el-menu-item>

      <el-menu-item
          v-for="widget in widgetsSortedByIndex"
          :key="widget.id"
          :index="widget.id"
          :style="getMenuItemStyle(widget)"
          class="hoverable-item"
      >
        <el-icon v-if="getIconComponent(widget)">
          <component :is="getIconComponent(widget)" />
        </el-icon>
        <span v-if="!collapsed">{{ widget.title }}</span>
      </el-menu-item>
    </el-menu>

    <div class="widget-content">
      <el-scrollbar class="widget-scroll-wrapper">
        <DynamicWidget
            v-if="activeWidget"
            :key="activeWidget.id"
            :data="activeWidget"
            :ref="el => setWidgetRef(activeWidget.id, el)"
        />
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, resolveComponent } from 'vue'
import { useRoute } from 'vue-router'
import type { WidgetUnion } from '@/types/widgets'
import DynamicWidget from '@/views/widgets/dynamic-widget.vue'
import { getWidgetStyle, getHeaderColor, getBodyColor } from '@/utils/widgetColorIconManager'

// 路由实例
const route = useRoute()

// 响应式状态
const activeWidgetId = ref('')
const collapsed = ref(false)
const widgetRefs = new Map<string, any>()

// 模拟数据 - TODO: 从后端获取
const widgets: WidgetUnion[] = [
  {
    id: '1',
    index: 1,
    type: 'notepdf',
    title: '互动式课件 [自定义title]',
    createTime: '2025-03-01T12:00:00Z',
    updateTime: '2025-03-02T12:00:00Z',
    visible: true,
    editor: null,
    pdfFile: {
      fileName: '为什么开水和凉水听起来不一样.pdf',
      url: 'https://arxiv.org/pdf/2403.14740',
    },
    notes: [
      { page: 1, x: 100, y: 100, text: '毕导：为什么开水和凉水听起来不一样' },
    ],
  },
  {
    id: '2',
    index: 2,
    type: 'doc',
    title: '富文本文档 [自定义title]',
    createTime: '2025-03-01T12:00:00Z',
    updateTime: '2025-03-02T12:00:00Z',
    visible: true,
    editor: null,
    content: '# 本项目 UI 组件为\n\n<img src="https://element-plus.org/images/element-plus-logo.svg" width="75"/>',
    attachments: [
      { fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe' },
      { fileName: '伪7zip.pdf', url: 'https://www.7-zip.org/a/7z2409-arm64.exe' },
    ],
  },
  {
    id: '3',
    index: 3,
    type: 'assignment',
    title: '作业 [自定义title]',
    createTime: '2025-03-01T12:00:00Z',
    updateTime: '2025-03-02T12:00:00Z',
    visible: true,
    argueId: 0,
    editor: null,
    content: '# 我是作业\n\n请完成作业',
    attachments: [
      { fileName: '真7zip.exe', url: 'https://www.7-zip.org/a/7z2409-arm64.exe' },
    ],
    submitTypes: ['file', 'code'],
    submittedAssignment: null,
    status: 'pending',
  },
];

const title: string = '课程资源区'

const widgetsSortedByIndex = computed(() => {
  return [...widgets].sort((a, b) => a.index - b.index)
})

const activeWidget = computed(() => {
  return widgets.find(w => w.id === activeWidgetId.value)
})

const getMenuItemStyle = (widget: WidgetUnion) => {
  const color = getWidgetStyle(widget.type).color
  return {
    backgroundColor: widget.id === activeWidgetId.value
        ? getHeaderColor(color)
        : getBodyColor(color),
    color: widget.id === activeWidgetId.value ? 'white' : 'black',
    fontWeight: 'bold',
    borderRadius: '6px',
    margin: '4px 8px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    justifyContent: collapsed.value ? 'center' : 'flex-start',
    transition: 'all 0.2s',
  }
}

const getIconComponent = (widget: WidgetUnion) => {
  const iconName = getWidgetStyle(widget.type).icon
  return resolveComponent(iconName)
}

const toggleCollapse = () => {
  collapsed.value = !collapsed.value
}

const setWidgetRef = (id: string, el: any) => {
  if (el) widgetRefs.set(id, el)
}

const initActiveWidget = () => {
  const widgetId = route.query.widget as string
  const matched = widgets.find(w => w.id === widgetId)
  if (matched) {
    activeWidgetId.value = matched.id
  } else if (widgets.length > 0) {
    const minWidget = widgetsSortedByIndex.value[0]
    activeWidgetId.value = minWidget.id
  }
}

const handleMenuSelect = (widgetId: string) => {
  if (widgetId === '__toggle') return

  activeWidgetId.value = widgetId
  setTimeout(() => {
    widgetRefs.get(widgetId)?.init?.()
  }, 50)
}

onMounted(() => {
  initActiveWidget()
  setTimeout(() => {
    widgetRefs.get(activeWidgetId.value)?.init?.()
  }, 50)
})
</script>

<style scoped>
.widget-layout {
  display: flex;
  height: 100%;
  width: 100%;
}

.widget-menu {
  height: 100%;
  border-right: 1px solid #ebeef5;
  transition: width 0.3s ease-in-out;
  will-change: width;
}

.widget-menu:not(.el-menu--collapse) {
  width: 300px;
}

:deep(.el-menu--collapse) {
  width: 64px;
  transition: width 0.3s ease-in-out;
}

:deep(.el-menu-item), :deep(.el-sub-menu__title) {
  transition: padding 0.3s ease-in-out;
}

.el-menu--collapse {
  transition: width 0.3s ease-in-out !important;
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

.hoverable-item:hover {
  filter: brightness(1.08);
  cursor: pointer;
}
</style>