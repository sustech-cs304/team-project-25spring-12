<template>
  <el-row :gutter="20">
    <!-- 左侧：课程列表 -->
    <el-col :span="12">
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
    </el-col>

    <!-- 右侧：通知 + 日历 -->
    <el-col :span="12">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon style="margin-right: 8px;">
              <Calendar/>
            </el-icon>
            DDL 日历
          </div>
        </template>
        <DeadlineCalendarWidget/>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts" name="homepage">
import CourseListWidget from '@/views/components/homepage-course-cards.vue'
import DeadlineCalendarWidget from '@/views/components/hoempage-deadline-calendar.vue'
import {Calendar, Collection} from '@element-plus/icons-vue'
</script>

<style scoped>
.card-header {
  font-weight: bold;
  font-size: 16px;
  display: flex;
  align-items: center;
}
</style>