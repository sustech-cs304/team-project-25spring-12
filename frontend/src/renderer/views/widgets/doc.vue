<template>
  <widget-card :title="computedTitle" color="green" icon="Document">
    <md-and-file :fileList="props.data.attachments" :content="props.data.content" />
  </widget-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import widgetCard from './utils/widget-card.vue';
import MdAndFile from './utils/md-and-file.vue';
import type { DocWidget } from '@/types/widgets';

const props = defineProps<{
  data: DocWidget;
}>();

const computedTitle = computed(() => props.data?.title || '富文本展示区');
</script>