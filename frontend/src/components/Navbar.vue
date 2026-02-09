<template>
  <a-layout-header class="header">
    <div class="header-content">
      <div class="logo">
        <a href="/">
          <img src="@/assets/logo.png" alt="暖心商城" class="logo-img" />
          <span class="logo-text">暖心商城</span>
        </a>
      </div>
      
      <a-menu mode="horizontal" v-model="current" class="nav-menu">
        <a-menu-item key="home">
          <a href="/">首页</a>
        </a-menu-item>
        <a-sub-menu key="categories">
          <span slot="title">商品分类</span>
          <a-menu-item v-for="category in categories" :key="category.id">
            <a :href="`/category/${category.id}`">{{ category.name }}</a>
          </a-menu-item>
        </a-sub-menu>
        <a-menu-item key="hot">
          <a href="/hot">热门商品</a>
        </a-menu-item>
      </a-menu>
      
      <div class="header-right">
        <a-input-search 
          placeholder="搜索商品" 
          enter-button 
          class="search-input"
          @search="handleSearch"
        />
        
        <a-dropdown v-if="isAuthenticated">
          <a class="nav-item">
            <a-icon type="shopping-cart" />
            <span class="cart-count" v-if="cartCount > 0">{{ cartCount }}</span>
          </a>
          <a-menu slot="overlay">
            <a-menu-item>
              <a href="/cart">我的购物车</a>
            </a-menu-item>
          </a-menu>
        </a-dropdown>
        
        <a-dropdown v-if="isAuthenticated">
          <a class="nav-item">
            <a-icon type="user" />
            <span>{{ userInfo.username }}</span>
          </a>
          <a-menu slot="overlay">
            <a-menu-item>
              <a href="/user/profile">个人中心</a>
            </a-menu-item>
            <a-menu-item>
              <a href="/user/orders">我的订单</a>
            </a-menu-item>
            <a-menu-item v-if="isAdmin">
              <a href="/admin/dashboard">后台管理</a>
            </a-menu-item>
            <a-menu-divider />
            <a-menu-item @click="handleLogout">
              <a-icon type="logout" />
              <span>退出登录</span>
            </a-menu-item>
          </a-menu>
        </a-dropdown>
        
        <a href="/login" class="nav-item" v-else>
          <a-icon type="user" />
          <span>登录/注册</span>
        </a>
      </div>
    </div>
  </a-layout-header>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Navbar',
  data() {
    return {
      current: 'home',
      categories: []
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isAdmin', 'userInfo', 'cartCount'])
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    ...mapActions(['logout']),
    
    // 获取分类列表
    async fetchCategories() {
      try {
        const response = await this.$axios.get('/categories/')
        this.categories = response
      } catch (error) {
        console.error('获取分类失败:', error)
      }
    },
    
    // 搜索商品
    handleSearch(value) {
      if (value) {
        this.$router.push({ path: '/search', query: { keyword: value } })
      }
    },
    
    // 退出登录
    handleLogout() {
      this.$confirm({
        title: '确认退出',
        content: '确定要退出登录吗？',
        onOk: () => {
          this.logout()
          this.$message.success('退出成功')
          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style scoped>
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo a {
  display: flex;
  align-items: center;
  color: #1890ff;
  text-decoration: none;
}

.logo-img {
  height: 40px;
  margin-right: 10px;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
}

.nav-menu {
  flex: 1;
  margin: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.search-input {
  width: 250px;
  margin-right: 20px;
}

.nav-item {
  margin-left: 20px;
  cursor: pointer;
  color: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
}

.nav-item:hover {
  color: #1890ff;
}

.cart-count {
  background: #f5222d;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  position: relative;
  top: -8px;
  right: -5px;
}
</style>