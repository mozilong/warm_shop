# 基础镜像：Python3.11
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如MySQL客户端、编译依赖）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装Python依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制后端代码
COPY backend/ .

# 暴露端口（根据后端框架调整，如Flask默认5000，Django默认8000）
EXPOSE 8000

# 启动命令（根据实际启动方式调整）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]