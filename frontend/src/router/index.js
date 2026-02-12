import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import GoodsDetail from '../views/GoodsDetail.vue'
import Category from '../views/Category.vue'
import Cart from '../views/Cart.vue'
import Profile from '../views/Profile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/goods/:id', name: 'GoodsDetail', component: GoodsDetail },
  { path: '/category', name: 'Category', component: Category },
  { 
    path: '/cart', 
    name: 'Cart', 
    component: Cart,
    meta: { requiresAuth: true } // 需要登录
  },
  { 
    path: '/profile', 
    name: 'Profile', 
    component: Profile,
    meta: { requiresAuth: true } // 需要登录
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录用户无法访问需要权限的页面
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('token')
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
