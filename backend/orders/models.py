from django.db import models
from users.models import User
from goods.models import Goods

class Order(models.Model):
    """订单模型"""
    ORDER_STATUS = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('shipped', '已发货'),
        ('received', '已收货'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    )
    order_sn = models.CharField(max_length=32, unique=True, verbose_name='订单编号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name='订单状态')
    shipping_address = models.TextField(verbose_name='收货地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_sn

class OrderItem(models.Model):
    """订单商品模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='购买价格')
    quantity = models.IntegerField(verbose_name='购买数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_order_item'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return f'{self.order.order_sn} - {self.goods.name}'
    
    @property
    def total_price(self):
        """计算商品小计"""
        return self.price * self.quantity