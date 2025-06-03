<template>
  <div class="page">
    <div class="feeds-page">
      <div class="channel-container">
        <div class="scroll-container channel-scroll-container">
          <div class="content-container">
            <div class="left-channels">
              <div
                v-for="channel in leftChannels"
                :key="channel"
                class="channel"
                :class="{ active: activeChannel === channel }"
                @click="setActiveChannel(channel)"
              >
                {{ channel }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 内容区域 -->
      <div class="content-area">
        <!-- <p>当前显示：{{ activeChannel }} 的内容</p> -->
        <v3-waterfall
          :list="list"
          :colWidth="280"
          :virtual-time="400"
          :scrollBodySelector="isLimit ? '.limit-box' : ''"
          :isMounted="isMounted"
          :isLoading="loading"
          :isOver="over"
          class="waterfall"
          @scrollReachBottom="getNext"
        >
          <template v-slot:default="slotProp">
            <div class="list-item">
              <a :href="'#/argue/' + slotProp.item.argueId">
                <!-- <a :href="'https://gkshi.com/blog/' + slotProp.item._id"> -->
                <div class="cover-wrapper">
                  <!-- 此处注意：data-key 是该图片的字段名称，目前只支持在一级的字段，不支持嵌套 -->
                  <img v-if="slotProp.item.cover" :src="slotProp.item.cover" data-key="cover" class="cover" />
                </div>
                <div class="brief">
                  <h3>{{ slotProp.item.title }}</h3>
                  <p>{{ slotProp.item.outline }}</p>
                </div>
                <div class="cover-wrapper">
                  <img :src="slotProp.item.notExistSrc" data-key="notExistSrc" class="cover" />
                </div>
              </a>
              <div class="outline-bottom">
                <time>{{ slotProp.item.time }}</time>
                <p class="article-tags">
                  <!-- <span>tags</span> -->
                  <span v-for="tag of slotProp.item.tags" :key="tag" class="tag">{{
                    tag
                    }}
                  </span>
                </p>
                <p class='watch-info'><el-icon><Pointer /></el-icon><br>{{ slotProp.item.ratio }}%</p>
                <p class='watch-info'><el-icon><View/></el-icon><br>{{ slotProp.item.watch }}</p>
              </div>
            </div>
          </template>
        </v3-waterfall>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import service from '../../utils/request';

// const list = ref([]);
const list = ref([
  {
    title: '标题',
    outline: '摘要',
    tags: ['课程', '任课老师', '发起者'],
    time: '25-01-14',
  },
  {
    title: '标题',
    outline: '摘要',
    tags: ['课程', '任课老师', '发起者'],
    time: '25-05-14',
  },
])

// 格式化后端数据到前端所需格式
const formatList = (rawList) => {
  return rawList.map(item => ({
    argueId: item.id,
    title: item.title,
    outline: item.content.length > 100 ? item.content.slice(0, 100) + '...' : item.content, // 截取前100字符作为摘要
    tags: [item.status, item.editor.username],
    time: item.updateTime,
    ratio: item.support + item.notSupport === 0 ? '?' :
      (item.support / (item.support + item.notSupport)).toFixed(2) * 100,
    watch: item.watch,
  }));
};

const fetchList = async (channel) => {
  try {
    const response = await service.get('/argue');
    console.log('fetchList', response.data);
    list.value = formatList(response.data || []);;
  } catch (error) {
    console.error('获取数据失败:', error);
  }
};

const getNext = async () => {
  // NO NEED
};

// 左侧 channel 列表
// const leftChannels = ['广场', '我的'];
const leftChannels = ['广场'];
// 当前激活的 channel
const activeChannel = ref('广场');

// 设置激活的 channel
const setActiveChannel = (channel) => {
  activeChannel.value = channel;
};

onMounted(() => {
  fetchList(activeChannel.value);
});

</script>


<style scoped>
/* FeedChannels 样式 */
.page {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}
.feeds-page {
  padding: 20px;
}
.channel-container {
  border-bottom: 1px solid #e0e0e0;
}
.scroll-container {
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}
.content-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
}
.left-channels {
  display: flex;
  gap: 10px;
}
.channel {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  color: #333;
  transition: all 0.2s ease;
}
.channel:hover {
  background-color: #f5f5f5;
}
.channel.active {
  font-weight: bold;
  color: #007bff;
  border-bottom: 2px solid #007bff;
}
.content-area {
  margin-top: 20px;
}

/* 瀑布流容器 */
.waterfall {
  margin: 0 auto;
  padding: 0 10px;
}

/* 卡片容器 */
.list-item {
  width: 280px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-bottom: 16px;
}
.list-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 文章摘要区域 */
.brief {
  padding: 16px;
}
.brief h3 {
  margin: 0;
  font-size: 18px;
  line-height: 1.4;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.brief p {
  margin: 8px 0 0;
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 增加到 3 行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 底部区域 */
.outline-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  border-top: 1px solid #eee;
}
.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 0;
  font-size: 12px;
  color: #999;
}
.article-tags > span:first-child {
  margin-right: 4px;
}
.tag {
  background: #f5f5f5;
  border-radius: 4px;
  padding: 2px 6px;
}
.watch-info {
  font-size: 12px;
  color: #666;
  margin: 0 8px;
}
time {
  font-size: 12px;
  color: #999;
}
/* 链接样式 */
.list-item a {
  text-decoration: none;
  color: inherit;
  display: block;
}

/* 响应式调整 */
@media (max-width: 600px) {
  .list-item {
    width: 100%;
    max-width: 280px;
  }
  .brief h3 {
    font-size: 16px;
  }
  .brief p {
    font-size: 13px;
    -webkit-line-clamp: 2; /* 移动端限制 2 行 */
  }
}
</style>