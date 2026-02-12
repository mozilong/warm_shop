<template>
  <div class="goods-detail-page">
    <div class="goods-detail-container">
      <div class="goods-image">
        <img :src="goodsDetail.image" :alt="goodsDetail.name" />
      </div>
      <div class="goods-info">
        <h2>{{ goodsDetail.name }}</h2>
        <p class="price">¥{{ goodsDetail.price }}</p>
        <p class="description">{{ goodsDetail.description }}</p>
        <div class="quantity">
          <label for="quantity">数量：</label>
          <input type="number" id="quantity" v-model.number="quantity" min="1" />
        </div>
        <button class="add-to-cart-btn" @click="addToCart">加入购物车</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../utils/request'

const route = useRoute()
const router = useRouter()
const goodsId = route.params.id
const goodsDetail = ref({})
const quantity = ref(1)

const fetchGoodsDetail = async () => {
  try {
    const res = await request.get(`/goods/${goodsId}`)
    if (res.code === 200) {
      goodsDetail.value = res.data
    } else {
      alert('商品不存在')
      router.push('/')
    }
  } catch (err) {
    console.error(err)
    alert('获取商品详情失败')
    router.push('/')
  }
}

const addToCart = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('请先登录')
    router.push('/login')
    return
  }
  try {
    const res = await request.post('/cart/add', {
      goodsId: goodsId,
      quantity: quantity.value
    })
    if (res.code === 200) {
      alert('加入购物车成功')
    } else {
      alert(res.message)
    }
  } catch (err) {
    console.error(err)
    alert('加入购物车失败')
  }
}

onMounted(() => fetchGoodsDetail())
</script>

<style scoped>
.goods-detail-page {
  flex: 1;
  background-color: #ffebee;
  min-height: calc(100vh - 120px);
  padding: 2rem;
}
.goods-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(255, 107, 129, 0.3);
}
.goods-image {
  flex: 1;
}
.goods-image img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
}
.goods-info {
  flex: 1;
}
.goods-info h2 {
  color: #e63946;
  margin-bottom: 1rem;
}
.goods-info .price {
  color: #e63946;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
}
.goods-info .description {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}
.quantity {
  margin-bottom: 2rem;
}
.quantity label {
  margin-right: 1rem;
  color: #333;
}
.quantity input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.add-to-cart-btn {
  padding: 1rem 2rem;
  background: #ff6b81;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.3s;
}
.add-to-cart-btn:hover {
  background: #e63946;
}
</style>
