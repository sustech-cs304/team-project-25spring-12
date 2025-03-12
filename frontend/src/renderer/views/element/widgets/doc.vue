<template>
  <widget-card :title="computedTitle" color="green" icon="Document">
    <md-and-file :data="props.data"/>
  </widget-card>
</template>

<script setup lang="ts">
import {computed, defineProps, ref} from "vue";
import widgetCard from "./widget-card.vue";
import MdAndFile from "./md-and-file.vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const computedTitle = computed(() => props.data?.title || "富文本展示区");
</script>