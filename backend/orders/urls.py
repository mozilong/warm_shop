from django.urls import path
from . import views  # 改为导入整个views模块，避免指定不存在的类

urlpatterns = [
    path('create/', views.order_create, name='order_create'),  # 创建订单
    path('', views.order_list, name='order_list'),            # 订单列表
    path('express/<int:order_id>/', views.order_express, name='order_express'),  # 物流信息
]
