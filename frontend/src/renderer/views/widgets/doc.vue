<template>
  <widget-card :title="computedTitle" type="doc" :callback="authenticated ? handleEdit : undefined">
    <md-and-file-editor :fileList="props.data.attachments" :content="props.data.content" v-if="isEditing" />
    <md-and-file :fileList="props.data.attachments" :content="props.data.content" v-else />
    <template #button>
      <template v-if="isEditing">
        <el-icon><Check/></el-icon>
        <span>保存</span>
      </template>
      <template v-else>
        <el-icon><Edit/></el-icon>
        <span>编辑</span>
      </template>
    </template>
  </widget-card>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue';
import widgetCard from './utils/widget-card.vue';
import MdAndFile from './utils/md-and-file.vue';
import MdAndFileEditor from './utils/md-and-file-editor.vue';
import type { DocWidget } from '@/types/widgets';

const props = defineProps<{
  data: DocWidget;
}>();

const computedTitle = computed(() => props.data?.title || '富文本展示区');
const authenticated = ref(true);
const isEditing = ref(false);

const handleEdit = () => {
  isEditing.value = !isEditing.value;
  // TODO: 确认保存内容逻辑完善
}

defineExpose({
  init: () => {}
});
</script>