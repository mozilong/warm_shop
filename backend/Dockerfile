# 基础镜像：Python 3.9 alpine（轻量，适配Django 3.2，兼容CentOS 7）
FROM python:3.9-alpine

# 设置工作目录
WORKDIR /app

# 安装系统依赖（解决MySQL/Pillow编译问题）
RUN apk add --no-cache gcc musl-dev mysql-dev libffi-dev openssl-dev python3-dev jpeg-dev zlib-dev

# 设置Python环境变量（避免缓存pyc文件）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # 时区配置
    TZ=Asia/Shanghai

# 安装Python依赖（国内源加速）
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制后端代码
COPY . .

# 收集静态文件（生产环境必备）
RUN python manage.py collectstatic --noinput

# 暴露端口（与docker-compose映射一致）
EXPOSE 8000

# 启动命令：Gunicorn（生产环境，替代runserver）
CMD ["gunicorn", "warm_shop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
