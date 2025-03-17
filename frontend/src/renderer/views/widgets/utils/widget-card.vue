<template>
  <el-card class="widget-card">
    <template #header>
      <div class="card-header">
        <el-icon v-if="iconComponent" class="card-icon">
          <component :is="iconComponent" />
        </el-icon>
        <span>{{ title }}</span>
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
-->

<script setup>
import { computed, resolveComponent } from 'vue'

const props = defineProps({
  title: String,
  icon: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['red', 'green', 'blue', 'purple', 'orange', 'teal', 'gray'].includes(value),
  },
})

const headerColor = computed(() => {
  return {
    red: '#F87171',
    green: '#34D399',
    blue: '#60A5FA',
    purple: '#A78BFA',
    orange: '#FB923C',
    teal: '#2DD4BF',
    gray: '#9CA3AF',
  }[props.color] || '#60A5FA'
})

const bodyColor = computed(() => {
  return {
    red: '#FEE2E2',
    green: '#D1FAE5',
    blue: '#DBEAFE',
    purple: '#EDE9FE',
    orange: '#FFEDD5',
    teal: '#CCFBF1',
    gray: '#E5E7EB',
  }[props.color] || '#DBEAFE'
})

const iconComponent = computed(() => {
  return props.icon ? resolveComponent(props.icon) : null
})
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
  gap: 8px;
  color: white;
  font-size: 16px;
  font-weight: bold;
  padding: 12px 16px;
  border-radius: 12px 12px 0 0;
}

.card-icon {
  font-size: 20px;
}
</style>
