<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="logo">
        <img src="/assets/logo.png" alt="暖心表白墙商城" />
        <span class="logo-text">暖心表白墙商城</span>
      </div>
      <ul class="nav-links">
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/category">商品分类</router-link></li>
        <li v-if="isLoggedIn"><router-link to="/cart">购物车</router-link></li>
        <li v-if="isLoggedIn"><router-link to="/profile">个人中心</router-link></li>
        <li v-if="!isLoggedIn"><router-link to="/login">登录</router-link></li>
        <li v-if="!isLoggedIn"><router-link to="/register">注册</router-link></li>
        <li v-if="isLoggedIn" @click="handleLogout" class="logout-btn">退出登录</li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  isLoggedIn.value = false
  alert('退出登录成功')
  router.push('/')
}

onMounted(() => checkLoginStatus())
</script>

<style scoped>
.navbar {
  background-color: #ff6b81;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
}
.logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.logo img {
  height: 50px;
  width: 50px;
  border-radius: 50%;
  object-fit: cover;
}
.logo-text {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}
.nav-links {
  display: flex;
  list-style: none;
  gap: 2rem;
}
.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s;
}
.nav-links a:hover {
  color: #ffebee;
}
.logout-btn {
  color: white;
  cursor: pointer;
  font-size: 1.1rem;
  transition: color 0.3s;
}
.logout-btn:hover {
  color: #ffebee;
}
</style>
