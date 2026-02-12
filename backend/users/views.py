from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm  # 现在能正常导入
from .models import User

# 注册视图
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册成功！请登录')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# 登录视图（重命名为user_login，避免和内置login冲突）
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 尝试通过用户名/手机号登录
            try:
                if username.isdigit() and len(username) == 11:
                    user = User.objects.get(phone=username)
                else:
                    user = User.objects.get(username=username)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                auth_login(request, user)  # 使用Django内置登录
                messages.success(request, '登录成功！')
                return redirect('home')
            else:
                messages.error(request, '密码错误！')
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# 退出登录
def user_logout(request):
    auth_logout(request)
    messages.success(request, '已退出登录！')
    return redirect('home')

# 个人中心
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'profile.html', {'user': request.user})
