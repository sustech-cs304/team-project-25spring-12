<template>
  <mark-assignment-list :course-id="courseId" :widgets="widgets" />
</template>

<script setup lang="ts" name="mark-class">
import MarkAssignmentList from "@/views/widgets/mark-assignment-list.vue";
import {AssignmentWidget} from "@/types/widgets";
import {Folder} from "@/types/folder";
import {Page} from "@/types/page";
import {getFolders} from "@/api/course";
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {getPage} from "@/api/courseMaterial";

const route = useRoute();

const courseId = ref(0);
const widgets = ref<AssignmentWidget[]>([]);

onMounted(async () => {
  courseId.value = Number(route.params.courseId);
  const response = await getFolders(courseId.value);
  const folders = response.data as Folder[];
  folders.forEach((folder) => {
    folder.pages.forEach(async (pageItem) => {
      const response = await getPage(pageItem.id);
      const page = response.data as Page;
      page.widgets.forEach((widget) => {
        if (widget.type === "assignment") {
          const assignmentWidget = widget as AssignmentWidget;
          if (assignmentWidget.submitType === "file") {
            widgets.value.push(assignmentWidget);
          }
        }
      });
    });
  });
});
</script>

<style scoped>

</style>