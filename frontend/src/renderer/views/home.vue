<template>
  <div class="wrapper">
    <Header/>
    <div class="content-box">
      <Tabs/>
      <div class="content">
        <router-view v-slot="{ Component, route }">
          <keep-alive :include="cachedViews">
            <component
                :is="Component"
                :key="route.fullPath"
            />
          </keep-alive>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {useTabsStore} from '@/store/tabs';
import {computed} from "vue";
import Header from '@/components/header.vue';
import Tabs from '@/components/tabs.vue';

const tabs = useTabsStore();
const cachedViews = computed(() => tabs.nameList)
</script>

<style>
.wrapper {
  height: 100vh;
  overflow: hidden;
}

.content-box {
  position: absolute;
  left: 0;
  right: 0;
  top: 70px;
  bottom: 0;
  padding-bottom: 30px;
  -webkit-transition: left 0.3s ease-in-out;
  transition: left 0.3s ease-in-out;
  background: #eef0fc;
  overflow: hidden;
}

.content {
  width: auto;
  height: 100%;
  padding: 20px;
  overflow-y: scroll;
  box-sizing: border-box;
}

.content::-webkit-scrollbar {
  width: 0;
}
</style>
