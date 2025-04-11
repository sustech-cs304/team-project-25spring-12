<template>
  <component :is="Component" v-bind="{ data }" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { widgetMap } from '@/types/widgets'
import type { WidgetUnion } from '@/types/widgets'

const props = defineProps<{
  data: WidgetUnion;
}>()

const Component = computed(() => widgetMap[props.data.type])
</script>
