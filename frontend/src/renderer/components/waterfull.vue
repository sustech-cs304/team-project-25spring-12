<template>
    <Waterfall :lazyload="false" :breakpoints="breakpoints" :gutter="8" :list="list" :column-count="3">
      <template #item="{ item }">
        <div class="card_content">
          <div class="card_img" :class="{ active: !item.goodsPicture && !item.storePicture }">
            <LazyImg class="cover" :url="item.src" />
          </div>
          <div>
            title
          </div>
        </div>
      </template>
    </Waterfall>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  import { LazyImg, Waterfall } from 'vue-waterfall-plugin-next'
  import 'vue-waterfall-plugin-next/dist/style.css'
  const props = defineProps({
    productList: {
      type: Array
    }
  })
  
  const list = computed(() => {
    return props.productList
  })
  const breakpoints = ref({
    3000: {
      //当屏幕宽度小于等于3000
      rowPerView: 8, // 一行8图
    },
    1800: {
      //当屏幕宽度小于等于1800
      rowPerView: 6,// 一行6图
    },
    1200: {
      //当屏幕宽度小于等于1200
      rowPerView: 4,
    },
  
    500: {
      //当屏幕宽度小于等于500
      rowPerView: 2,
    },
  })
  
  
  </script>
  
  <style lang="scss" scoped>
  .card_content {
    border-radius: 4px;
    background: #fff;
    box-sizing: border-box;
  
    .card_img {
      margin-bottom: 7px;
  
      &.active {
        border: 1px solid #e7e7e7;
      }
  
      :deep(.lazy__img) {
        width: 100%;
        border-radius: 4px;
        font-size: 0;
        height: 100%;
      }
    }
  
    .content {
      padding: 0 8px;
  
      .store {
        color: rgba(0, 0, 0, 0.4);
        font-size: 12px;
        font-weight: 400;
        margin-bottom: 4px;
      }
  
      .title {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 14px;
      }
  
      .tags {
        display: flex;
        flex-wrap: wrap;
  
        .tags-item {
          background: rgba(153, 151, 255, 0.05);
          border-radius: 2px;
          padding: 3px 4px;
          margin: 0 5px 5px 0;
          color: rgba(0, 0, 0, 0.4);
          font-size: 12px;
          border: 1px solid rgb(244, 244, 249);
  
          &:last-child {
            margin-right: 0;
          }
        }
      }
    }
  }
  </style>
  
  