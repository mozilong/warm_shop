# 阶段1：构建前端代码（使用Node 20.19.0 alpine，适配Vite 5.x，轻量且稳定）
FROM node:20.19.0-alpine AS build-stage
WORKDIR /app
# 安装依赖（添加国内源加速，解决构建慢的问题）
RUN npm config set registry https://registry.npmmirror.com
# 复制package.json和锁文件，利用Docker缓存（避免每次构建都重装依赖）
COPY package*.json ./
# 安装依赖（强制安装，忽略可选依赖错误）
RUN npm install --force
# 复制所有前端代码
COPY . .
# 构建前端（生产环境打包，添加--force跳过版本检查）
RUN npm run build --force

# 阶段2：用Nginx运行前端（轻量，不受Node版本影响）
FROM nginx:1.24-alpine AS production-stage
# 复制构建好的前端文件到Nginx默认目录
COPY --from=build-stage /app/dist /usr/share/nginx/html
# 复制自定义Nginx配置（解决前端路由刷新404问题）
COPY nginx.conf /etc/nginx/conf.d/default.conf
# 暴露端口
EXPOSE 80
# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
