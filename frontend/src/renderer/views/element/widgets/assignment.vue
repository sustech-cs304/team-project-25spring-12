<template>
  <widget-card :title="computedTitle" color="orange" icon="Notebook">
    <div class="container">
      <md-and-file :data="props.data" />

      <codemirror v-model="code" :options="options" />
    </div>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "./widget-card.vue";
import MdAndFile from "./md-and-file.vue";
import {computed, defineProps} from "vue";
import { ref } from 'vue';
import Codemirror from 'codemirror-editor-vue3';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/dracula.css'; // 选择您喜欢的主题
import 'codemirror/mode/javascript/javascript.js';
import 'codemirror/mode/python/python.js';

const code = ref('// 在此编写您的代码...');
const options = {
  mode: 'javascript', // 默认模式
  theme: 'dracula', // 选择主题
  lineNumbers: true,
  // 其他配置项
};

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const computedTitle = computed(() => props.data?.title || "作业");


</script>

<style scoped>

</style>