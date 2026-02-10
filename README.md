# WARM_SHOP

轻量级前后端分离电商后端系统，基于 Django + DRF 开发，适配中小商家快速搭建线上商城，支持自定义用户体系、商品管理、购物车、订单、支付对接等核心电商能力，兼顾开发效率与生产环境适配性。
## 技术栈
### 核心技术
后端框架：Django 3.2 + Django REST Framework (DRF) 3.14  
认证机制：JWT (djangorestframework-simplejwt)  
数据库：MySQL 5.7+/8.0+（PyMySQL 驱动，兼容 utf8mb4）  
安全防护：登录失败限制 (django-axes)、跨域处理 (django-cors-headers)  
媒体处理：Pillow（头像 / 商品图片上传）  
部署适配：Gunicorn（WSGI 服务器）

### 环境要求
Python：3.8+（推荐 3.9）  
MySQL：5.7+/8.0+  
操作系统：Linux/macOS/Windows（推荐 Linux 生产环境）  
依赖管理：pip（推荐虚拟环境 venv/conda）

## 快速启动（开发者本地部署）
### 1. 克隆仓库
```bash
git clone https://github.com/mozilong/warm_shop.git
cd warm_shop
```
### 2. 搭建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
### 3. 安装后端依赖
```bash
cd backend
pip install -r ../requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
### 4. 数据库初始化
```bash
# 1. 登录 MySQL（输入 root 密码）
mysql -uroot -p

# 2. 创建数据库（指定 utf8mb4 编码，兼容特殊字符）
CREATE DATABASE IF NOT EXISTS warm_shop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. 授权用户（替换密码为自定义值）
GRANT ALL PRIVILEGES ON warm_shop.* TO 'warm_shop_user'@'%' IDENTIFIED BY 'ShopUser123!';
FLUSH PRIVILEGES;
EXIT;
```
### 5. 配置项目参数（可选）
修改 backend/warm_shop/settings.py 中的核心配置（支持环境变量，生产环境推荐用环境变量）：
```bash
# Linux/macOS 临时环境变量（示例）
export DB_NAME=warm_shop
export DB_USER=warm_shop_user
export DB_PASSWORD=你的自定义密码
export DB_HOST=localhost
export DB_PORT=3306
export DJANGO_DEBUG=False  # 生产环境设为 False
export DJANGO_SECRET_KEY=你的随机密钥  # 推荐用 django-admin startproject 生成
```
### 6. 数据库迁移（创建表结构）
```bash
#临时添加项目根目录到PYTHONPATH
export PYTHONPATH=/root/warm_shop:$PYTHONPATH

cd backend
# 优先生成用户模块迁移（解决外键依赖）
python manage.py makemigrations users
# 生成其他模块迁移
python manage.py makemigrations
# 执行迁移（创建表）
python manage.py migrate

# 创建超级管理员（用于后台管理）
python manage.py createsuperuser
# 按提示输入用户名、邮箱、密码
```
### 7. 启动开发服务器
```bash
# 允许所有IP访问，端口 8000
python manage.py runserver 0.0.0.0:8000
```
### 8. 验证启动结果
首页：访问 http://你的IP:8000/，可见暖心商城首页  
后台管理：访问 http://你的IP:8000/admin/，用超级管理员账号登录  
接口健康检查：访问 http://你的IP:8000/admin/goods/goods/，可见商品管理页面  
核心业务模块说明  

| 模块目录        | 核心功能                                                   | 核心功能                        |
| --------------- | ---------------------------------------------------------- | ------------------------------- |
| backend/users   | 自定义用户模型（手机号 / 头像扩展）、权限管理、JWT 认证    | 短信验证、第三方登录            |
| backend/goods   | 商品基础管理（名称 / 价格 / 库存 / 状态）、商品列表 / 详情 | 分类 / 标签、商品搜索、库存锁   |
| backend/carts   | 空骨架（待扩展）                                           | 购物车增删改查、库存预扣减      |
| backend/orders  | 空骨架（待扩展）                                           | 购物车增删改查、库存预扣减      |
| backend/payment | 空骨架（待扩展）                                           | 微信 / 支付宝支付对接、回调处理 |

## 关键配置说明
### 1. 核心配置文件
| 文件路径                      | 关键配置项                                                  |
| ----------------------------- | ----------------------------------------------------------- |
| backend/warm_shop/settings.py | 自定义用户模型：AUTH_USER_MODEL = 'users.User'              |
| 数据库配置                    | DATABASES（MySQL 连接信息）                                 |
| 跨域配置                      | CORS_ALLOW_ALL_ORIGINS（开发环境 True，生产环境需指定域名） |
| JWT 配置                      | SIMPLE_JWT（令牌有效期、加密算法）                          |
| 媒体文件                      | MEDIA_ROOT/MEDIA_URL（头像 / 商品图片存储路径）             |
| backend/warm_shop/urls.py     | 路由配置：首页、后台管理、媒体文件访问                      |

### 2. 生产环境关键调整
```python
# settings.py 生产环境配置示例
DEBUG = False
ALLOWED_HOSTS = ['www.warmshop.com', 'api.warmshop.com']  # 指定允许的域名
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # 从环境变量获取密钥
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://www.warmshop.com']  # 仅允许前端域名跨域

# 收集静态文件（admin 静态资源）
python manage.py collectstatic
```
### 3. 部署建议（生产环境）
```bash
# 使用 Gunicorn 启动 WSGI 服务
gunicorn warm_shop.wsgi:application --bind 0.0.0.0:8000 --workers 4
# 配合 Nginx 反向代理（处理静态文件、负载均衡）
```
## 常见问题（FAQ）
**Q1: 执行 migrate 报错 Cannot add foreign key constraint？**  
原因：自定义用户模型迁移未优先执行，导致外键依赖失败；  
解决方案：重置数据库 → 清理迁移文件 → 先执行 makemigrations users 再执行其他迁移（详见 README 末尾「兜底方案」）。  
**Q2: 访问 8000 端口显示 404？** 
原因：根路径未配置路由；  
解决方案：确认 backend/warm_shop/urls.py 中已添加首页路由 path('', home, name='home')。  
**Q3: 启动服务时报 AxesWarning: axes.W003？**  
原因：未配置 Axes 认证后端；  
解决方案：确认 settings.py 中 AUTHENTICATION_BACKENDS 包含 axes.backends.AxesBackend。
**Q4: 上传头像 / 商品图片后无法访问？**  
原因：媒体文件路由未配置；  
解决方案：确认 urls.py 中已添加 static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)。
**兜底方案（重置数据库）**  
若迁移过程中出现复杂错误，可重置数据库重新开始：

```bash
# 1. 删除数据库
mysql -uroot -p -e "DROP DATABASE IF EXISTS warm_shop; CREATE DATABASE warm_shop DEFAULT CHARSET utf8mb4;"

# 2. 清理迁移文件
cd backend
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# 3. 重新迁移
python manage.py makemigrations users
python manage.py makemigrations
python manage.py migrate
```

# 更新日志
v1.0.0（2026-02）  
初始版本，完成核心功能：  
自定义用户模型（手机号 / 头像扩展），解决与 Django 内置 User 冲突；  
商品基础模型（名称 / 价格 / 库存 / 状态）；  
首页与后台管理路由配置；  
DRF + JWT 认证、跨域、登录限制等基础配置；  
修复关键问题：迁移外键冲突、Axes 警告、首页 404 等。  
待迭代功能  
购物车模块：增删改查、库存预扣减；  
订单模块：订单创建 / 取消、物流轨迹对接；  
支付模块：微信 / 支付宝支付对接、回调处理；  
商品模块：分类 / 标签、搜索、图片多图上传；  
接口文档：集成 drf-spectacular 生成 OpenAPI 文档。