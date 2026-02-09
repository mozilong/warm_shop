from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer, CartUpdateSerializer
from goods.models import Goods

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        """只返回当前用户的购物车数据"""
        return Cart.objects.filter(user=self.request.user).select_related('goods')

    def get_serializer_class(self):
        """更新时使用简化序列化器"""
        if self.action in ['update', 'partial_update']:
            return CartUpdateSerializer
        return CartSerializer

    def create(self, request, *args, **kwargs):
        """创建购物车（已存在则更新数量）"""
        goods_id = request.data.get('goods_id')
        quantity = int(request.data.get('quantity', 1))

        # 验证商品是否存在且库存充足
        try:
            goods = Goods.objects.get(id=goods_id, is_active=True)
        except Goods.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if goods.stock < quantity:
            return Response({
                'code': 400,
                'message': '库存不足'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 查找或创建购物车记录
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            goods=goods,
            defaults={'quantity': quantity}
        )

        # 已存在则累加数量
        if not created:
            cart.quantity += quantity
            if cart.quantity > goods.stock:
                return Response({
                    'code': 400,
                    'message': '库存不足'
                }, status=status.HTTP_400_BAD_REQUEST)
            cart.save()

        serializer = self.get_serializer(cart)
        return Response({
            'code': 201 if created else 200,
            'message': '添加成功' if created else '更新成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)