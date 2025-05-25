<template>
  <el-card shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon style="margin-right: 8px;">
          <Collection/>
        </el-icon>
        课程列表
      </div>
    </template>
    <CourseListWidget/>
  </el-card>
</template>

<script setup lang="ts" name="mark-center">
import CourseListWidget from '@/views/components/mark-course-cards.vue'
import {Collection} from '@element-plus/icons-vue'
</script>

<style scoped>
.card-header {
  font-weight: bold;
  font-size: 16px;
  display: flex;
  align-items: center;
}
</style>
