import axios from 'axios'
import { Message, Modal } from 'ant-design-vue'
import store from '../store'
import router from '../router'

// 创建Axios实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：添加JWT令牌
service.interceptors.request.use(
  config => {
    const token = store.state.token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理响应和错误
service.interceptors.response.use(
  response => {
    // 直接返回响应数据
    return response.data
  },
  error => {
    const { response } = error
    
    // 未授权（401）：token过期或无效
    if (response && response.status === 401) {
      Modal.warning({
        title: '登录过期',
        content: '您的登录已过期，请重新登录',
        onOk: () => {
          store.dispatch('logout')
          router.push({ name: 'Login' })
        }
      })
    }
    
    // 权限不足（403）
    else if (response && response.status === 403) {
      Message.error('您没有权限执行此操作')
    }
    
    // 其他错误
    else {
      const errorMsg = response?.data?.message || response?.data?.error || '请求失败'
      Message.error(errorMsg)
    }
    
    return Promise.reject(error)
  }
)

export default service