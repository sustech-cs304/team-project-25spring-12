<template>
  <el-card class="widget-card">
    <template #header>
      <div class="card-header">
        <div class="card-title">
          <el-icon v-if="iconComponent" class="card-icon">
            <component :is="iconComponent" />
          </el-icon>
          <span>{{ title }}</span>
        </div>
        <el-button style="color: white" :color="headerColor" @click="callback" v-if="callback">
          <slot name="button" />
        </el-button>
      </div>
    </template>
    <slot />
  </el-card>
</template>

<!--
  widget-card

  一个可定制颜色和图标的卡片组件。
  本分支中，用于容纳 page 的各个组成部分（widgets），欢迎其他分支复用。
  - 颜色可选：red, green, blue, purple, orange, teal, gray
  - 支持自定义标题（title）和 Element Plus 图标（icon）

  @props {String} title - 标题
  @props {String} icon - Element Plus 图标名称
  @props {String} color - 预设颜色 (red, green, blue, purple, orange, teal, gray)
  @props {String} type - 使用 @/utils/widgetColorIconManager.ts 中的配色方案，方便在其他位置复用
  @props {Function} callback - 和 slot #button 一起启用后，右上角会有一个按钮
-->

<script setup lang="ts">
import { computed, resolveComponent } from 'vue'
import { getWidgetStyle, getHeaderColor, getBodyColor } from '@/utils/widgetColorIconManager'

const props = defineProps({
  title: String,
  icon: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: 'blue',
  },
  type: {
    type: String,
    default: '',
  },
  callback: {
    type: Function,
    default: undefined,
  }
})

const resolvedColor = computed(() => {
  return props.type ? getWidgetStyle(props.type).color : props.color
})
const resolvedIcon = computed(() => {
  return props.type ? getWidgetStyle(props.type).icon : props.icon
})

const headerColor = computed(() => getHeaderColor(resolvedColor.value))
const bodyColor = computed(() => getBodyColor(resolvedColor.value))
const iconComponent = computed(() =>
    resolvedIcon.value ? resolveComponent(resolvedIcon.value) : null
)
</script>

<style scoped>
.widget-card {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  padding: 0;
  border: none;
  background: none;
}

:deep(.el-card__header) {
  background-color: v-bind(headerColor) !important;
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
}

:deep(.el-card__body) {
  background-color: v-bind(bodyColor) !important;
  padding: 16px !important;
  margin: 0 !important;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: white;
  font-size: 16px;
  font-weight: bold;
  padding: 12px 16px;
  border-radius: 12px 12px 0 0;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-icon {
  font-size: 20px;
}
</style>
