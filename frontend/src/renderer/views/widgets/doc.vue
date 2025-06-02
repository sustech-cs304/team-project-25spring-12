<template>
  <widget-card :title="computedTitle" type="doc" :callback="callback">
    <md-and-file-editor
        @upload="handleUploadFile"
        @remove="handleRemoveFile"
        :fileList="form.attachments"
        :content="form.content"
        v-if="isEditing"/>
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
import {Check, Edit} from "@element-plus/icons-vue";
import {FileMeta} from "@/types/fileMeta";
import {editDocWidget} from "@/api/courseMaterial";

const props = defineProps<{
  data: DocWidget;
  canEdit: boolean;
}>();

const computedTitle = computed(() => props.data?.title || "文档");
const callback = computed(() => props.canEdit ? handleEdit : null)
const isEditing = ref(false);

const form = ref<DocWidget>(null);

const emit = defineEmits<{
  (e: "docUploadFile", file: FileMeta): void;
  (e: "docRemoveFile", file: FileMeta): void;
}>();

const handleEdit = async () => {
  if (isEditing.value) { // 点保存
    const response = await editDocWidget(form as DocWidget)
    console.log(response)
  } else { // 点编辑
    form.value = JSON.parse(JSON.stringify(props.data))
  }
  isEditing.value = !isEditing.value;
}

const handleUploadFile = (file: FileMeta) => {
  emit('docUploadFile', file)
}

const handleRemoveFile = (file: FileMeta) => {
  emit('docRemoveFile', file)
}

defineExpose({
  init: () => {}
});
</script>