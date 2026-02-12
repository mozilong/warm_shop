<template>
  <div class="goods-container">
    <el-card title="商品列表">
      <el-row :gutter="20">
        <el-col :span="6" v-for="goods in goodsList" :key="goods.id">
          <el-card>
            <img :src="goods.image" class="goods-img" />
            <div class="goods-name">{{ goods.name }}</div>
            <div class="goods-price">¥{{ goods.price }}</div>
            <el-button type="primary" size="small" @click="addToCart(goods.id)">加入购物车</el-button>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../utils/request'
import { ElMessage } from 'element-plus'

const goodsList = ref([])

// 加载商品列表（调用后端goods模块API）
const loadGoods = async () => {
  try {
    const res = await request.get('/goods/')
    goodsList.value = res.results  // DRF分页返回的列表
  } catch (err) {
    ElMessage.error('加载商品失败：' + err.message)
  }
}

// 加入购物车（调用后端carts模块API）
const addToCart = async (goodsId) => {
  try {
    await request.post('/carts/', { goods_id: goodsId, count: 1 })
    ElMessage.success('加入购物车成功')
  } catch (err) {
    ElMessage.error('加入购物车失败：' + err.message)
  }
}

onMounted(() => loadGoods())
</script>

<style scoped>
.goods-container {
  padding: 20px;
}
.goods-img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
.goods-name {
  margin: 10px 0;
  font-size: 14px;
}
.goods-price {
  color: red;
  font-weight: bold;
  margin-bottom: 10px;
}
</style>