from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
# 新增：导入重定向视图
from django.views.generic import RedirectView

urlpatterns = [
    # 新增：根路径/ 重定向到/admin/（后台管理页）
    path('', RedirectView.as_view(url='/admin/')),

    path('admin/', admin.site.urls),
    path('api/v1/commodity/', include(('commodity.urls', 'commodity'), namespace='commodity')),
    path('api/v1/shopper/', include(('shopper.urls', 'shopper'), namespace='shopper')),
    # 配置媒体资源的路由信息
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # 定义静态资源的路由信息
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
