<template>
  <div class="page">
    <div class="container" id="main">
      <productCard :productList="productList"></productCard>
      <div class="loading-text" v-if="loading">加载中...</div>
      <div class="loading-text" v-if="finish">没有更多了</div>
    </div>
  </div>
</template>


<script setup>
import productCard from '../../components/waterfull.vue'
const loading = ref(false)
const finish = ref(false)
let arr = [
  {
    id: 1,
    src: 'https://img.beiqiai.com/img1.jpg'
  },
  {
    id: 2,
    src: 'https://img.beiqiai.com/img2.jpg'
  },
  {
    id: 3,
    src: 'https://img.beiqiai.com/img3.jpg'
  },
  {
    id: 4,
    src: 'https://img.beiqiai.com/img4.jpg'
  },
  {
    id: 5,
    src: 'https://img.beiqiai.com/img5.jpg'
  },
  {
    id: 6,
    src: 'https://img.beiqiai.com/img6.jpg'
  },
  {
    id: 7,
    src: 'https://img.beiqiai.com/img7.jpg'
  },
  {
    id: 8,
    src: 'https://img.beiqiai.com/img8.jpg'
  },
  {
    id: 9,
    src: 'https://img.beiqiai.com/img9.jpg'
  },
  {
    id: 10,
    src: 'https://img.beiqiai.com/img10.jpg'
  },
  {
    id: 11,
    src: 'https://img.beiqiai.com/img11.jpg'
  },
  {
    id: 12,
    src: 'https://img.beiqiai.com/img12.jpg'
  },
  {
    id: 13,
    src: 'https://img.beiqiai.com/img13.jpg'
  },
  {
    id: 14,
    src: 'https://img.beiqiai.com/img14.jpg'
  },
  {
    id: 15,
    src: 'https://img.beiqiai.com/img15.jpg'
  },
  {
    id: 16,
    src: 'https://img.beiqiai.com/img16.jpg'
  },
  {
    id: 17,
    src: 'https://img.beiqiai.com/img17.jpg'
  },
  {
    id: 18,
    src: 'https://img.beiqiai.com/img18.jpg'
  },
  {
    id: 19,
    src: 'https://img.beiqiai.com/img19.jpg'
  },
  {
    id: 20,
    src: 'https://img.beiqiai.com/img20.jpg'
  },
  {
    id: 21,
    src: 'https://img.beiqiai.com/img21.jpg'
  },
  {
    id: 22,
    src: 'https://img.beiqiai.com/img22.jpg'
  },
  {
    id: 23,
    src: 'https://img.beiqiai.com/img23.jpg'
  },
  {
    id: 24,
    src: 'https://img.beiqiai.com/img24.jpg'
  },
  {
    id: 25,
    src: 'https://img.beiqiai.com/img25.jpg'
  }

]

let productList = ref([
  {
    id: 1,
    src: 'https://img.beiqiai.com/img1.jpg'
  },
  {
    id: 2,
    src: 'https://img.beiqiai.com/img2.jpg'
  },
  {
    id: 3,
    src: 'https://img.beiqiai.com/img3.jpg'
  },
  {
    id: 4,
    src: 'https://img.beiqiai.com/img4.jpg'
  },
  {
    id: 5,
    src: 'https://img.beiqiai.com/img5.jpg'
  },
  {
    id: 6,
    src: 'https://img.beiqiai.com/img6.jpg'
  },
  {
    id: 7,
    src: 'https://img.beiqiai.com/img7.jpg'
  },
  {
    id: 8,
    src: 'https://img.beiqiai.com/img8.jpg'
  },
  {
    id: 9,
    src: 'https://img.beiqiai.com/img9.jpg'
  },
  {
    id: 10,
    src: 'https://img.beiqiai.com/img10.jpg'
  },
  {
    id: 11,
    src: 'https://img.beiqiai.com/img11.jpg'
  },
  {
    id: 12,
    src: 'https://img.beiqiai.com/img12.jpg'
  },
  {
    id: 13,
    src: 'https://img.beiqiai.com/img13.jpg'
  },
  {
    id: 14,
    src: 'https://img.beiqiai.com/img14.jpg'
  },
  {
    id: 15,
    src: 'https://img.beiqiai.com/img15.jpg'
  },
  {
    id: 16,
    src: 'https://img.beiqiai.com/img16.jpg'
  },
  {
    id: 17,
    src: 'https://img.beiqiai.com/img17.jpg'
  },
  {
    id: 18,
    src: 'https://img.beiqiai.com/img18.jpg'
  },
  {
    id: 19,
    src: 'https://img.beiqiai.com/img19.jpg'
  },
  {
    id: 20,
    src: 'https://img.beiqiai.com/img20.jpg'
  },
  {
    id: 21,
    src: 'https://img.beiqiai.com/img21.jpg'
  },
  {
    id: 22,
    src: 'https://img.beiqiai.com/img22.jpg'
  },
  {
    id: 23,
    src: 'https://img.beiqiai.com/img23.jpg'
  },
  {
    id: 24,
    src: 'https://img.beiqiai.com/img24.jpg'
  },
  {
    id: 25,
    src: 'https://img.beiqiai.com/img25.jpg'
  }

])

//获取接口数据
const getProduct = () => {
  loading.value = true
  productList.value = [...productList.value, ...arr]
}
const handleScroll = () => {
  const scrollHeight = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)
  //滚动条滚动距离
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
  //窗口可视范围高度
  const clientHeight =
    window.innerHeight || Math.min(document.documentElement.clientHeight, document.body.clientHeight)
  if ((clientHeight + scrollTop) + 100 >= scrollHeight) {
    //快到底时----加载
    getProduct()
  }
}

const debounce = (fn, delay) => {
  let timeout
  return function () {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      fn.apply(this, arguments)
    }, delay)
  }
}
onMounted(() => {
  window.addEventListener('scroll', debounce(handleScroll, 1000))
})
</script>


<style lang="scss" scoped>
.loading-text {
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  z-index: 999;
  margin: auto;
  padding: 20px 0;
  font-size: 16px;
}

:deep(.waterfall-list) {
  background: none;
}

.container {
  padding: 0 12px;
}
</style>


<style scoped>
  .page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
</style>

