# carts/urls.py
from django.urls import path
# 导入实际存在的视图函数，而非CartViewSet
from .views import cart_add, cart_list, cart_delete

urlpatterns = [
    path('add/<int:goods_id>/', cart_add, name='cart_add'),
    path('list/', cart_list, name='cart_list'),
    path('delete/<int:cart_id>/', cart_delete, name='cart_delete'),
]
