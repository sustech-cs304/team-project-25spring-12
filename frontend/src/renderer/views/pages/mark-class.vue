<template>
  <mark-assignment-list
      :course-id="courseId"
      :course-name="courseName"
      :widgets="widgetsSorted"
  />
</template>

<script setup lang="ts" name="mark-class">
import MarkAssignmentList from "@/views/widgets/mark-assignment-list.vue";
import {AssignmentWidget} from "@/types/widgets";
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {getAllAssignments, getWidget} from "@/api/feedback";
import {getCourse} from "@/api/course";
import {Course} from "@/types/course";

const route = useRoute();

const courseId = ref(0);
const courseName = ref("");
const widgets = ref<AssignmentWidget[]>([]);
const widgetsSorted = computed(() => [...widgets.value].sort((a, b) => a.id - b.id));

onMounted(async () => {
  courseId.value = Number(route.params.courseId);
  const courseResponse = await getCourse(courseId.value);
  const course = courseResponse.data as Course;
  courseName.value = course.name;
  const assignmentsResponse = await getAllAssignments(courseId.value);
  widgets.value = assignmentsResponse.data as AssignmentWidget[];
});
</script>

<style scoped>

</style>