<template>
  <component
      :is="Component"
      v-bind="{ data }"
      ref="innerWidgetRef"
  />
</template>

<script setup lang="ts">
import {computed, ref} from 'vue'
import {widgetMap} from '@/types/widgets'
import type {WidgetUnion} from '@/types/widgets'

const props = defineProps<{
  data: WidgetUnion;
}>()

const Component = computed(() => widgetMap[props.data.type]);

const innerWidgetRef = ref<any>(null);

defineExpose({
  init: () => {
    innerWidgetRef.value?.init?.();
  }
});
</script>
