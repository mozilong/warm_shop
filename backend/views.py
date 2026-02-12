# /app/views.py 修复版
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.apps import apps
from django.db import IntegrityError
import json
import re
import hashlib
import random

# 导入自定义用户模型
User = apps.get_model(*'users.User'.split('.'))

# 手机号正则校验
PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')

# 统一响应函数
def api_response(code, message, data=None, status=None):
    response_data = {
        "code": code,
        "message": message,
        "data": data or {}
    }
    return JsonResponse(response_data, status=status or (200 if code == 200 else 400))

# 手机号格式校验
def validate_phone(phone):
    if phone and not PHONE_PATTERN.match(phone):
        return False
    return True

# 首页接口
def home(request):
    return api_response(200, "首页接口")

# 分类接口
def category(request):
    return api_response(200, "分类接口")

# 注册接口
@csrf_exempt
def register(request):
    try:
        if request.method != "POST":
            return api_response(400, "仅支持POST请求", status=400)
        
        if not request.body:
            return api_response(400, "请求体不能为空", status=400)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return api_response(400, "JSON格式错误", status=400)
        
        # 提取参数
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip() or None

        # 基础校验
        if not username or not password:
            return api_response(400, "用户名/密码不能为空")
        if len(password) < 6:
            return api_response(400, "密码长度不能少于6位")
        if phone and not validate_phone(phone):
            return api_response(400, "手机号格式错误（11位有效号码）")
        
        # 唯一性校验
        if User.objects.filter(username=username).exists():
            return api_response(400, "用户名已存在")
        if phone and User.objects.filter(phone=phone).exists():
            return api_response(400, "该手机号已注册")
        
        # 创建用户
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                phone=phone,
                email=email,
                is_active=True
            )
        except IntegrityError as e:
            print(f"注册数据库错误：{str(e)}")
            return api_response(400, "注册失败：用户名/手机号/邮箱已存在", status=400)
        
        return api_response(
            200, "注册成功",
            data={"user_id": user.id, "username": user.username, "phone": user.phone}
        )
    
    except Exception as e:
        print(f"注册系统异常：{str(e)}")
        return api_response(500, "注册失败：系统内部错误", status=500)

# 登录接口（核心修复：传入 request）
@csrf_exempt
def login(request):
    try:
        if request.method != "POST":
            return api_response(400, "仅支持POST请求", status=400)
        
        if not request.body:
            return api_response(400, "请求体不能为空", status=400)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return api_response(400, "JSON格式错误", status=400)
        
        # 提取参数
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        
        if not username or not password:
            return api_response(400, "用户名/密码不能为空")
        
        # 关键修复：authenticate 传入 request 参数，兼容 AxesBackend
        user = authenticate(request, username=username, password=password)
        if not user:
            return api_response(401, "账号或密码错误", status=401)
        
        # 生成安全 Token
        token_seed = f"{user.id}_{user.username}_{random.randint(100000, 999999)}"
        token = hashlib.sha256(token_seed.encode()).hexdigest()
        
        return api_response(
            200, "登录成功",
            data={
                "token": token,
                "user": {"id": user.id, "username": user.username}
            }
        )
    
    except Exception as e:
        print(f"登录系统异常：{str(e)}")
        return api_response(500, "登录失败：系统内部错误", status=500)
