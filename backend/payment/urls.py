from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    # 模拟支付回调接口
    path('payment/<int:pk>/mock-pay/', PaymentViewSet.as_view({'get': 'mock_pay'}), name='mock-pay'),
    # 创建支付订单接口（绑定订单ID）
    path('order/<int:order_id>/payment/', PaymentViewSet.as_view({'post': 'create'}), name='order-payment'),
]