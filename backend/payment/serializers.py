from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderSerializer

class PaymentSerializer(serializers.ModelSerializer):
    order_info = OrderSerializer(source='order', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_info', 'payment_no', 'payment_method', 
                  'amount', 'status', 'payment_time', 'trade_no']
        read_only_fields = ['id', 'payment_no', 'status', 'payment_time', 'trade_no']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_method']