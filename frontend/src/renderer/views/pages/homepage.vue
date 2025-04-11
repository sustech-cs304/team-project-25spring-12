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
      <el-card shadow="hover" style="margin-top: 20px;">
        <template #header>
          <div class="card-header">
            <el-icon style="margin-right: 8px;">
              <MessageBox/>
            </el-icon>
            最新通知
          </div>
        </template>
        <MessageBoxWidget/>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import CourseListWidget from '@/views/element/homepage-course-cards.vue'
import MessageBoxWidget from '@/views/element/homepage-message-box.vue'
import DeadlineCalendarWidget from '@/views/element/hoempage-deadline-calendar.vue'
import {MessageBox, Calendar, Collection} from '@element-plus/icons-vue'
</script>

<style scoped>
.card-header {
  font-weight: bold;
  font-size: 16px;
  display: flex;
  align-items: center;
}
</style>