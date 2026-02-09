# 基础镜像：Python 3.9 轻量版
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（解决 mysqlclient 编译依赖）
RUN apt update && apt install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖（使用清华源加速）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
COPY . .

# 创建媒体文件和静态文件目录
RUN mkdir -p /app/media /app/staticfiles /app/logs

# 暴露端口（Django 默认 8000）
EXPOSE 8000

# 启动命令（生产环境使用 gunicorn）
CMD ["gunicorn", "warm_shop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]