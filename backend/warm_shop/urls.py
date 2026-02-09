"""warm_shop URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# 导入首页视图
from backend.views import home

urlpatterns = [
    # 根路径（首页）
    path('', home, name='home'),
    # 后台管理
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 媒体文件访问路由