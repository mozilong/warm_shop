import Vue from 'vue'
import Vuex from 'vuex'
import axios from '../utils/request'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || '',
    refreshToken: localStorage.getItem('refreshToken') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || {},
    cartCount: 0
  },
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.userInfo.is_staff || false,
    cartCount: state => state.cartCount
  },
  mutations: {
    SET_TOKEN(state, tokens) {
      state.token = tokens.access
      state.refreshToken = tokens.refresh
      localStorage.setItem('token', tokens.access)
      localStorage.setItem('refreshToken', tokens.refresh)
    },
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    SET_CART_COUNT(state, count) {
      state.cartCount = count
    },
    LOGOUT(state) {
      state.token = ''
      state.refreshToken = ''
      state.userInfo = {}
      state.cartCount = 0
      localStorage.clear()
    }
  },
  actions: {
    // 登录
    async login({ commit }, credentials) {
      const response = await axios.post('/users/login/', credentials)
      if (response.code === 200) {
        commit('SET_TOKEN', response.data)
        // 获取用户信息
        await this.dispatch('getUserInfo')
        // 获取购物车数量
        await this.dispatch('getCartCount')
      }
      return response
    },

    // 注册
    async register({ commit }, userData) {
      const response = await axios.post('/users/register/', userData)
      return response
    },

    // 获取用户信息
    async getUserInfo({ commit }) {
      try {
        const response = await axios.get('/users/me/')
        if (response.code === 200) {
          commit('SET_USER_INFO', response.data)
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    },

    // 获取购物车数量
    async getCartCount({ commit }) {
      try {
        const response = await axios.get('/cart/')
        commit('SET_CART_COUNT', response.length)
      } catch (error) {
        console.error('获取购物车数量失败:', error)
      }
    },

    // 登出
    logout({ commit }) {
      commit('LOGOUT')
    }
  },
  modules: {}
})