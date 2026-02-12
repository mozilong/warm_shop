import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  // 配置路径别名（确保@指向src目录）
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  // 开发服务器配置（可选，不影响构建）
  server: {
    port: 8080,
    host: '0.0.0.0'
  }
})
