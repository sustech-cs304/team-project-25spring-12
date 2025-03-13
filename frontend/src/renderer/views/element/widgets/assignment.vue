<template>
  <widget-card :title="computedTitle" color="orange" icon="Notebook">
    <div class="container">
      <md-and-file :data="props.data"/>

      <div class="code-editor">
        <div class="toolbar">
          <span class="el-text">选择语言：</span>
          <el-select v-model="selectedLanguage" size="small" @change="updateMode">
            <el-option v-for="lang in languages" :key="lang.value" :label="lang.label" :value="lang.value" />
          </el-select>

          <span class="el-text">Tab 长度：</span>
          <el-select v-model="tabSize" placeholder="Tab 长度" size="small">
            <el-option v-for="size in tabSizes" :key="size" :label="`${size} 空格`" :value="size" />
          </el-select>

          <el-button type="primary" :icon="Upload" @click="submitCode" class="submit-btn">提交</el-button>
        </div>

        <codemirror v-model="code" :options="options"/>
      </div>

      <div class="homework-editor">
        <md-and-file-editor :data="props.data"/>
      </div>

    </div>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "./widget-card.vue";
import MdAndFile from "./md-and-file.vue";
import {computed, ref} from "vue";
import {Upload} from "@element-plus/icons-vue";
import Codemirror from "codemirror-editor-vue3";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/dracula.css";

import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/python/python.js";
import "codemirror/mode/clike/clike.js";
import MdAndFileEditor from "@/views/element/widgets/md-and-file-editor.vue";  // Java, C++, C

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const languages = [
  {label: "C++", value: "text/x-c++src"},
  {label: "Java", value: "text/x-java"},
  {label: "Python", value: "python"},
];

const computedTitle = computed(() => props.data?.title || "作业");

const code = ref("");
const selectedLanguage = ref("text/x-c++src");
const tabSizes = [2, 4, 8];
const tabSize = ref(4);

const options = computed(() => ({
  mode: selectedLanguage.value,
  theme: "dracula",
  lineNumbers: true,
  tabSize: tabSize.value,
  indentUnit: tabSize.value,
  indentWithTabs: true,
  autoCloseBrackets: true,
}));

const updateMode = () => {
  options.value.mode = selectedLanguage.value;
};

const submitCode = () => {
  console.log(code.value);
  // TODO: 上传到后端
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  padding: 0;
  background-color: transparent;
  border: none;
  gap: 15px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 15px;
  background-color: white;
}

.code-editor {
  display: flex;
  flex-direction: column;
  height: 700px;
  overflow: hidden;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.code-editor :deep(.CodeMirror) {
  height: 100%;
}

.toolbar {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 10px;
}

.el-text {
  margin-right: 8px;
  font-size: 14px;
  color: #606266;
}

.el-select {
  width: 120px;
  margin-right: 20px;
}

.submit-btn {
  margin-left: auto;
  margin-right: 20px;
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
}

.submit-btn:hover {
  background-color: #66b1ff;
}
</style>
