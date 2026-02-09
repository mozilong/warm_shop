from rest_framework import serializers
from .models import Cart
from goods.serializers import GoodsListSerializer

class CartSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer(read_only=True)
    goods_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'goods', 'goods_id', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']

    def get_total_price(self, obj):
        """计算单条购物车商品总价"""
        return obj.goods.price * obj.quantity

class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity']

    def validate_quantity(self, value):
        """验证数量大于0"""
        if value <= 0:
            raise serializers.ValidationError("数量必须大于0")
        return value