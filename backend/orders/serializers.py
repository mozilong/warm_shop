import uuid
from django.utils import timezone
from rest_framework import serializers
from .models import Order, OrderItem
from goods.models import Goods
from goods.serializers import GoodsListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer(read_only=True)
    goods_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'goods', 'goods_id', 'price', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']

class OrderCreateSerializer(serializers.ModelSerializer):
    """创建订单序列化器"""
    items = OrderItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'shipping_address', 'items']
        read_only_fields = ['id']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # 生成订单编号
        order_sn = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
        
        # 计算订单总金额
        total_amount = 0
        order_items = []
        
        # 验证商品并创建订单项
        for item_data in items_data:
            goods_id = item_data.pop('goods_id')
            quantity = item_data['quantity']
            
            try:
                goods = Goods.objects.get(id=goods_id, is_active=True)
            except Goods.DoesNotExist:
                raise serializers.ValidationError(f'商品ID {goods_id} 不存在')
            
            if goods.stock < quantity:
                raise serializers.ValidationError(f'商品 {goods.name} 库存不足')
            
            # 计算商品总价
            item_total = goods.price * quantity
            total_amount += item_total
            
            # 创建订单项
            order_items.append({
                'goods': goods,
                'price': goods.price,
                'quantity': quantity
            })
            
            # 扣减库存
            goods.stock -= quantity
            goods.sales += quantity
            goods.save()
        
        # 创建订单
        order = Order.objects.create(
            user=user,
            order_sn=order_sn,
            total_amount=total_amount,
            **validated_data
        )
        
        # 创建订单项
        for item in order_items:
            OrderItem.objects.create(order=order, **item)
        
        return order

class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_sn', 'user_name', 'total_amount', 'status', 
                  'shipping_address', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_sn', 'total_amount', 'created_at', 'updated_at']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """更新订单状态序列化器"""
    class Meta:
        model = Order
        fields = ['status']