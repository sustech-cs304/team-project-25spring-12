<template>
  <div class="widget-layout">
    <!-- 菜单 + 切换按钮区域 -->
    <div class="widget-menu-wrapper" :class="{ collapsed }">
      <!-- 折叠按钮 -->
      <div class="menu-toggle" @click="toggleCollapse">
        <el-icon>
          <component :is="collapsed ? 'ArrowRightBold' : 'ArrowLeftBold'"/>
        </el-icon>
        <span v-if="showTitle" class="menu-title">{{ title }}</span>
      </div>

      <!-- 菜单栏 -->
      <el-menu
          class="widget-menu"
          :default-active="activeWidgetId"
          :collapse="collapsed"
          :collapse-transition="true"
          mode="vertical"
          @select="handleMenuSelect"
      >
        <el-menu-item
            v-for="widget in widgetsSortedByIndex"
            :key="widget.id"
            :index="widget.id"
            :style="getMenuItemStyle(widget)"
            class="hoverable-item"
        >
          <el-icon v-if="getIconComponent(widget)">
            <component :is="getIconComponent(widget)"/>
          </el-icon>
          <span v-if="!collapsed">{{ widget.title }}</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 内容区域 -->
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
import {computed, nextTick, onMounted, ref, resolveComponent, watch} from 'vue'
import {useRoute} from 'vue-router'
import type {Page} from "@/types/page";
import type {WidgetUnion} from '@/types/widgets'
import DynamicWidget from '@/views/widgets/dynamic-widget.vue'
import {getBodyColor, getHeaderColor, getWidgetStyle} from '@/utils/widgetColorIconManager'
import {getCourseMaterials} from "@/api/courseMaterial"

const route = useRoute()

const activeWidgetId = ref('')
const collapsed = ref(false)
const widgetRefs = new Map<string, any>()
const showTitle = ref(!collapsed.value)

const widgets = ref<WidgetUnion[]>([])
const title = ref('')

onMounted(async () => {
  const response = await getCourseMaterials()
  const data = response.data as Page
  title.value = data.name
  widgets.value = data.widgets
  initActiveWidget()
  setTimeout(() => {
    widgetRefs.get(activeWidgetId.value)?.init?.()
  }, 50)
})

const widgetsSortedByIndex = computed(() => {
  return [...widgets.value].sort((a, b) => a.index - b.index)
})

const activeWidget = computed(() => {
  return widgets.value.find(w => w.id === activeWidgetId.value)
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

const toggleCollapse = async () => {
  collapsed.value = !collapsed.value
  await nextTick()
}

const setWidgetRef = (id: string, el: any) => {
  if (el) widgetRefs.set(id, el)
}

const initActiveWidget = () => {
  const widgetId = route.query.widget as string
  const matched = widgets.value.find(w => w.id == widgetId)
  if (matched) {
    activeWidgetId.value = matched.id
  } else if (widgets.value.length > 0) {
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

watch(collapsed, (val) => {
  if (val) { // 收起菜单：立即隐藏文字
    showTitle.value = false
  } else { // 展开菜单：动画结束后显示文字
    setTimeout(() => {
      showTitle.value = true
    }, 300)
  }
})
</script>

<style scoped>
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

.widget-menu-wrapper.collapsed {
  width: 64px;
}

:deep(.el-menu--collapse) {
  width: 64px;
}

.menu-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  cursor: pointer;
  border-bottom: 1px solid #ebeef5;
  transition: padding 0.3s ease-in-out;
}

.menu-title {
  font-weight: bold;
  font-size: 16px;
  transition: opacity 0.3s ease;
  white-space: nowrap;
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