from django.db import models
from orders.models import Order

class Payment(models.Model):
    """支付记录模型"""
    PAYMENT_METHOD = (
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('unionpay', '银联支付'),
    )
    PAYMENT_STATUS = (
        ('pending', '待支付'),
        ('success', '支付成功'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_no = models.CharField(max_length=64, unique=True, verbose_name='支付单号')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, verbose_name='支付方式')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name='支付状态')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    trade_no = models.CharField(max_length=64, null=True, blank=True, verbose_name='第三方支付流水号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_payments'
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'

    def __str__(self):
        return self.payment_no