# 构建阶段：Node16
FROM node:16-alpine as build-stage

WORKDIR /app

# 复制前端依赖文件
COPY frontend/package*.json ./
RUN npm install --registry=https://registry.npm.taobao.org

# 复制前端代码并打包
COPY frontend/ .
RUN npm run build

# 生产阶段：Nginx部署静态文件
FROM nginx:alpine as production-stage

# 复制构建产物到Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html
# 复制自定义Nginx配置（可选）
# COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]