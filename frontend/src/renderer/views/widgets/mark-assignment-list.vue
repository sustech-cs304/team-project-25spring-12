<template>
  <widget-card title="作业选择" style="height: 100%">
    <el-scrollbar>
      <div class="widget-list">
        <div
            class="widget-item"
            v-for="widget in props.widgets"
            :key="widget.id"
            @click="handleWidgetClick(widget)"
        >
          <el-icon class="link-icon"><Document /></el-icon>
          <span class="widget-name">{{ widget.title }}</span>
        </div>
      </div>
    </el-scrollbar>
  </widget-card>
</template>

<script setup lang="ts">
import WidgetCard from "@/views/widgets/utils/widget-card.vue";
import {Document} from "@element-plus/icons-vue";
import {useRouter} from "vue-router"
import {AssignmentWidget} from "@/types/widgets";

const props = defineProps<{
  courseId: number;
  widgets: AssignmentWidget[];
}>();

const router = useRouter();

const handleWidgetClick = (widget: AssignmentWidget) => {
  router.push('/mark/' + props.courseId + "/widget/" + widget.id);
}
</script>

<style scoped>
.widget-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 4px 0;
}

.widget-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.widget-item:hover {
  background-color: #f5f7fa;
}

.link-icon {
  color: #409eff;
  font-size: 18px;
}

.widget-name {
  font-weight: 500;
  color: #333;
}
</style>
