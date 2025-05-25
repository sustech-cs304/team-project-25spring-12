<template>
  <mark-assignment-list :course-id="courseId" :widgets="widgetsSorted" />
</template>

<script setup lang="ts" name="mark-class">
import MarkAssignmentList from "@/views/widgets/mark-assignment-list.vue";
import {AssignmentWidget} from "@/types/widgets";
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {getAllAssignments, getWidget} from "@/api/feedback";

const route = useRoute();

const courseId = ref(0);
const widgets = ref<AssignmentWidget[]>([]);
const widgetsSorted = computed(() => [...widgets.value].sort((a, b) => a.id - b.id));

onMounted(async () => {
  courseId.value = Number(route.params.courseId);
  const response = await getAllAssignments(courseId.value);
  const widgetIds = response.data as number[];
  for (const widgetId of widgetIds) {
    const widgetResponse = await getWidget(widgetId);
    const widget = widgetResponse.data as AssignmentWidget;
    widgets.value.push(widget);
  }
});
</script>

<style scoped>

</style>