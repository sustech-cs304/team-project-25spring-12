<template>
  <component
      :is="Component"
      v-bind="{ data, editable, pageId }"
      ref="innerWidgetRef"
      @update="handleUpdate"
  />
</template>

<script setup lang="ts">
import {computed, DefineComponent, ref} from 'vue'
import {WidgetType} from '@/types/widgets'
import type {WidgetUnion} from '@/types/widgets'
import NotePdf from '@/views/widgets/notepdf.vue'
import Doc from '@/views/widgets/doc.vue'
import Assignment from '@/views/widgets/assignment.vue'

const props = defineProps<{
  data: WidgetUnion;
  editable: boolean;
  pageId: number,
}>()

const emit = defineEmits<{
  (e: "update", data: WidgetUnion): void;
}>();

const handleUpdate = (data: WidgetUnion) => {
  emit('update', data)
}

const widgetMap: Record<WidgetType, DefineComponent<any, any, any>> = {
  notepdf: NotePdf,
  doc: Doc,
  assignment: Assignment,
};
const Component = computed(() => widgetMap[props.data.type]);

const innerWidgetRef = ref<any>(null);

defineExpose({
  init: () => {
    innerWidgetRef.value?.init?.();
  }
});
</script>
