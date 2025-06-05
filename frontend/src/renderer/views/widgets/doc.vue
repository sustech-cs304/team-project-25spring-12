<template>
  <widget-card
      :title="computedTitle"
      type="doc"
      :button-visible="props.editable"
      @click="handleClick"
  >
    <!--  编辑中：使用 form 中暂存的数据  -->
    <div v-if="isEditing">
      <el-form :model="form" :rules="rules" label-width="120px">
        <!-- 内容标题 -->
        <el-form-item label="内容标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入内容标题"></el-input>
        </el-form-item>
      </el-form>
      <md-and-file-editor
          @upload="handleUploadFile"
          @remove="handleRemoveFile"
          :fileList="form.attachments"
          :content="form.content"
          ref="contentEditor"
      />
    </div>

    <!--  展示中：使用父组件注入的数据  -->
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
import {computed, onMounted, ref} from 'vue';
import widgetCard from './utils/widget-card.vue';
import MdAndFile from './utils/md-and-file.vue';
import MdAndFileEditor from './utils/md-and-file-editor.vue';
import type {DocWidget, WidgetUnion} from '@/types/widgets';
import {Check, Edit} from "@element-plus/icons-vue";
import {FileMeta} from "@/types/fileMeta";
import {addWidgetAttachment, createDocWidget, editDocWidget, removeWidgetAttachment} from "@/api/courseMaterial";
import {ElMessage} from "element-plus";

const props = defineProps<{
  pageId: number;
  data: DocWidget;
  editable: boolean;
}>();

onMounted(async () => {
  if (props.data.id === 0) await handleClick();
})

const contentEditor = ref<InstanceType<typeof MdAndFileEditor> | null>(null);
const computedTitle = computed(() => props.data?.title || "文档");
const isEditing = ref(false);

const form = ref<DocWidget>(null);
const rules = {
  title: [{required: true, message: '请输入内容标题', trigger: 'blur'}]
};

const emit = defineEmits<{
  (e: "update", data: WidgetUnion): void;
}>();

const handleClick = async () => {
  if (isEditing.value) { // 点保存
    form.value.content = contentEditor.value?.getContent();
    let message = "";

    const oldAttachments = props.data.attachments || [];
    const newAttachments = form.value.attachments || [];

    const addedFiles = newAttachments.filter(f => !oldAttachments.some(o => o.id === f.id));
    const removedFiles = oldAttachments.filter(f => !newAttachments.some(n => n.id === f.id));

    const editResponse = props.data.id === 0 ?
        await createDocWidget(form.value as DocWidget, props.pageId):
        await editDocWidget(form.value as DocWidget);
    if (editResponse.status !== 200) {
      message += "保存文本失败\n";
    }

    for (const file of addedFiles) {
      const res = await addWidgetAttachment(editResponse.data.id, file.id);
      if (res.status !== 200) message += `附件添加失败：${file.name}\n`;
    }

    for (const file of removedFiles) {
      const res = await removeWidgetAttachment(file.id);
      if (res.status !== 200) message += `附件删除失败：${file.name}\n`;
    }

    if (message !== "") {
      ElMessage.error(message);
    } else {
      ElMessage.success("保存成功");
      emit("update", editResponse.data);
    }

  } else { // 点编辑
    form.value = JSON.parse(JSON.stringify(props.data));
  }

  isEditing.value = !isEditing.value;
};

const handleUploadFile = async (file: FileMeta) => {
  const index = form.value.attachments.findIndex(f => f.id === file.id);
  if (index === -1) {
    form.value.attachments.push(file);
  }
}

const handleRemoveFile = async (file: FileMeta) => {
  const index = form.value.attachments.findIndex(f => f.id === file.id);
  if (index !== -1) {
    form.value.attachments.splice(index, 1);
  }
}

defineExpose({
  init: () => {}
});
</script>