from django.contrib import admin
from django.urls import path
# 导入我们写的JSON视图函数（根目录views.py）
from views import home, category, register, login  

urlpatterns = [
    path('admin/', admin.site.urls),
    # 核心：/register/ 指向我们写的register视图（返回JSON）
    path('register/', register),
    # 核心：/login/ 指向我们写的login视图（返回JSON）
    path('login/', login),
    # 其他原有路由（可保留）
    path('', home),
    path('category/', category),
    # 重点：删除所有其他指向模板注册页面的路由（如auth的register路由）
]
