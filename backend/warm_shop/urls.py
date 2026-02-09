from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户模块
    path('api/', include('users.urls')),
    # 商品模块
    path('api/', include('goods.urls')),
    # 购物车模块
    path('api/', include('carts.urls')),
    # 订单模块
    path('api/', include('orders.urls')),
    # 支付模块
    path('api/', include('payment.urls')),
    # 系统管理模块
    path('api/', include('system.urls')),
]

# 开发环境媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)