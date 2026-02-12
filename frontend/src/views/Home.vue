<template>
  <main class="home">
    <!-- 轮播图区域 -->
    <section class="carousel">
      <div class="carousel-item" v-for="(item, index) in carouselItems" :key="index">
        <img :src="item.image" :alt="item.title" />
        <div class="carousel-caption">{{ item.title }}</div>
      </div>
    </section>

    <!-- 商品分类区域 -->
    <section class="categories">
      <h2>热门分类</h2>
      <div class="category-grid">
        <div class="category-card" v-for="cat in categories" :key="cat.id">
          <img :src="cat.icon" :alt="cat.name" />
          <h3>{{ cat.name }}</h3>
        </div>
      </div>
    </section>

    <!-- 热门商品区域 -->
    <section class="hot-products">
      <h2>热门商品</h2>
      <div class="product-grid">
        <!-- 商品卡片：点击卡片跳转详情页，按钮单独处理加入购物车 -->
        <div 
          class="product-card" 
          v-for="product in hotProducts" 
          :key="product.id"
          @click="goToGoodsDetail(product.id)"
        >
          <img :src="product.image" :alt="product.name" />
          <h4>{{ product.name }}</h4>
          <p class="price">¥{{ product.price }}</p>
          <!-- stop阻止冒泡：避免点击按钮时触发卡片跳转 -->
          <button 
            class="add-to-cart" 
            @click.stop="addToCart(product.id)"
          >
            加入购物车
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
// 导入Vue核心方法和路由
import { ref } from 'vue'
import { useRouter } from 'vue-router'
// 导入封装的请求工具
import request from '../utils/request'

// 初始化路由实例
const router = useRouter()

// 1. 轮播图数据（可替换为自己的图片链接）
const carouselItems = ref([
  {
    title: '520限定礼盒',
    image: 'https://picsum.photos/1200/400?random=1'
  },
  {
    title: '表白专属礼品',
    image: 'https://picsum.photos/1200/400?random=2'
  },
  {
    title: '情侣定制周边',
    image: 'https://picsum.photos/1200/400?random=3'
  }
])

// 2. 商品分类数据
const categories = ref([
  { id: 1, name: '表白礼盒', icon: 'https://picsum.photos/100/100?random=10' },
  { id: 2, name: '情侣饰品', icon: 'https://picsum.photos/100/100?random=11' },
  { id: 3, name: '定制周边', icon: 'https://picsum.photos/100/100?random=12' },
  { id: 4, name: '浪漫花束', icon: 'https://picsum.photos/100/100?random=13' }
])

// 3. 热门商品数据
const hotProducts = ref([
  { id: 1, name: '520爱心礼盒', price: 199, image: 'https://picsum.photos/200/200?random=20' },
  { id: 2, name: '情侣对戒', price: 299, image: 'https://picsum.photos/200/200?random=21' },
  { id: 3, name: '定制钥匙扣', price: 59, image: 'https://picsum.photos/200/200?random=22' },
  { id: 4, name: '玫瑰永生花', price: 129, image: 'https://picsum.photos/200/200?random=23' }
])

// 4. 跳转到商品详情页方法
const goToGoodsDetail = (id) => {
  router.push(`/goods/${id}`)
}

// 5. 加入购物车方法（含登录校验）
const addToCart = async (goodsId) => {
  // 校验是否登录
  const token = localStorage.getItem('token')
  if (!token) {
    alert('请先登录后再添加商品～')
    router.push('/login')
    return
  }

  // 已登录则调用接口添加购物车
  try {
    const res = await request.post('/cart/add', {
      goodsId: goodsId,
      quantity: 1 // 默认添加1件
    })
    if (res.code === 200) {
      alert('加入购物车成功！')
    } else {
      alert(`添加失败：${res.message}`)
    }
  } catch (err) {
    console.error('加入购物车出错：', err)
    alert('网络异常，添加购物车失败～')
  }
}
</script>

<style scoped>
/* 页面基础样式 */
.home {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* 轮播图样式 */
.carousel {
  height: 400px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.carousel-item {
  position: relative;
  height: 100%;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  bottom: 2rem;
  left: 2rem;
  color: white;
  font-size: 2rem;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

/* 商品分类样式 */
.categories {
  margin-bottom: 3rem;
}

.categories h2 {
  color: #e63946; /* logo同色系红色 */
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
}

.category-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.3s;
  cursor: pointer;
}

.category-card:hover {
  transform: translateY(-5px);
}

.category-card img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 1rem;
}

/* 热门商品样式 */
.hot-products h2 {
  color: #e63946;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.3s;
  cursor: pointer; /* 鼠标悬浮显示手型，提示可点击 */
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(255, 107, 129, 0.3);
}

.product-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-card h4 {
  padding: 1rem;
  font-size: 1.1rem;
}

.product-card .price {
  color: #e63946;
  font-size: 1.3rem;
  font-weight: bold;
  padding: 0 1rem 1rem;
}

.add-to-cart {
  width: 100%;
  padding: 0.8rem;
  background-color: #ff6b81; /* logo同色系粉色 */
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-to-cart:hover {
  background-color: #e63946;
}
</style>
