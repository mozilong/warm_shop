// /root/warm_shop/frontend/src/utils/request.js
import axios from 'axios'

// 创建axios实例
const request = axios.create({
  // 基础路径：对应Nginx转发的/api前缀（前端请求会自动加/api）
  baseURL: '/api',
  // 请求超时时间
  timeout: 10000,
  // 请求头默认配置
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器（可选，添加token等）
request.interceptors.request.use(
  (config) => {
    // 登录后可从本地存储获取token，添加到请求头
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器（统一处理后端返回）
request.interceptors.response.use(
  (response) => {
    // 直接返回后端的响应数据（简化前端处理）
    return response.data
  },
  (error) => {
    // 统一处理错误提示
    console.error('请求错误：', error)
    // 提取后端返回的错误信息
    const errMsg = error.response?.data?.message || '请求失败，请稍后重试'
    // 前端弹窗提示（适配你的项目UI）
    alert(errMsg)
    return Promise.reject(error)
  }
)

// 导出request实例（供页面导入使用）
export default request
