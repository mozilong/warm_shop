from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import uuid
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from orders.models import Order

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """只返回当前用户的支付记录"""
        return Payment.objects.filter(order__user=self.request.user).select_related('order')

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        """创建支付订单（模拟第三方支付跳转）"""
        order_id = kwargs.get('order_id')
        try:
            # 验证订单是否存在且属于当前用户
            order = Order.objects.get(id=order_id, user=request.user)
            # 验证订单状态（只能支付待支付状态的订单）
            if order.status != 'pending':
                return Response({
                    'code': 400,
                    'message': '该订单无法支付'
                }, status=status.HTTP_400_BAD_REQUEST)
            # 检查是否已创建支付记录
            if hasattr(order, 'payment'):
                return Response({
                    'code': 400,
                    'message': '该订单已创建支付记录'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({
                'code': 404,
                'message': '订单不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 创建支付记录
        payment = Payment.objects.create(
            order=order,
            payment_no=f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}",
            payment_method=serializer.validated_data['payment_method'],
            amount=order.total_amount
        )

        # 模拟第三方支付链接（实际项目需对接真实支付接口）
        payment_url = f"/api/payment/{payment.id}/mock-pay"
        return Response({
            'code': 201,
            'message': '支付订单创建成功',
            'data': {
                "payment_id": payment.id,
                "payment_no": payment.payment_no,
                "payment_url": payment_url,
                "amount": payment.amount
            }
        }, status=status.HTTP_201_CREATED)

    def mock_pay(self, request, *args, **kwargs):
        """模拟支付成功回调"""
        payment_id = kwargs.get('pk')
        try:
            payment = Payment.objects.get(id=payment_id, order__user=self.request.user)
            if payment.status == 'success':
                return Response({
                    'code': 400,
                    'message': '该订单已支付成功'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新支付状态和订单状态
            payment.status = 'success'
            payment.payment_time = timezone.now()
            payment.trade_no = f"TRADE{uuid.uuid4().hex[:16].upper()}"
            payment.save()

            # 更新订单状态为已支付
            order = payment.order
            order.status = 'paid'
            order.save()

            return Response({
                'code': 200,
                'message': '支付成功',
                'data': {
                    "payment_no": payment.payment_no,
                    "trade_no": payment.trade_no,
                    "payment_time": payment.payment_time
                }
            })
        except Payment.DoesNotExist:
            return Response({
                'code': 404,
                'message': '支付记录不存在'
            }, status=status.HTTP_404_NOT_FOUND)