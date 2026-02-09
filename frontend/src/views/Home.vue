<template>
  <div class="home">
    <!-- 轮播图 -->
    <a-carousel autoplay effect="fade" class="carousel">
      <div v-for="(item, index) in carouselImages" :key="index">
        <img :src="item" alt="轮播图" class="carousel-img" />
      </div>
    </a-carousel>
    
    <!-- 分类导航 -->
    <div class="category-nav">
      <div class="container">
        <h2 class="section-title">商品分类</h2>
        <div class="category-list">
          <a v-for="category in categories" :key="category.id" :href="`/category/${category.id}`" class="category-item">
            <div class="category-icon">
              <a-icon type="appstore" />
            </div>
            <div class="category-name">{{ category.name }}</div>
          </a>
        </div>
      </div>
    </div>
    
    <!-- 推荐商品 -->
    <div class="recommend-goods">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">为你推荐</h2>
          <a href="/all-goods" class="view-more">查看更多</a>
        </div>
        <div class="goods-list">
          <a-card hoverable class="goods-card" v-for="goods in recommendGoods" :key="goods.id" :href="`/goods/${goods.id}`">
            <a-image :src="goods.image" alt="商品图片" class="goods-img" />
            <div class="goods-info">
              <h3 class="goods-name">{{ goods.name }}</h3>
              <div class="goods-price">¥{{ goods.price.toFixed(2) }}</div>
              <div class="goods-sales">销量：{{ goods.sales }}</div>
            </div>
          </a-card>
        </div>
      </div>