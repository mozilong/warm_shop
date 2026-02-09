from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer, OrderStatusUpdateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """订单视图集"""
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderStatusUpdateSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return [IsAuthenticated()]
        elif self.action in ['create', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        """普通用户只能查看自己的订单，管理员可以查看所有订单"""
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('items', 'items__goods')
        return Order.objects.filter(user=self.request.user).prefetch_related('items', 'items__goods')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # 返回完整订单信息
        order_serializer = OrderSerializer(order)
        return Response({
            'code': 201,
            'message': '订单创建成功',
            'data': order_serializer.data
        }, status=status.HTTP_201_CREATED)