from django.db import models
from users.models import User
from goods.models import Goods
import uuid

class Order(models.Model):
    """订单模型（示例，需与你实际字段一致）"""
    ORDER_STATUS = (
        ('UNPAID', '未支付'),
        ('PAID', '已支付'),
        ('SHIPPED', '已发货'),
        ('COMPLETED', '已完成'),
        ('CANCELED', '已取消'),
    )
    
    # 核心字段（根据你的实际模型调整）
    order_number = models.CharField(max_length=64, verbose_name='订单编号', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='下单用户')
    goods_item = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品单价')
    quantity = models.IntegerField(default=1, verbose_name='购买数量')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    status = models.CharField(max_length=16, choices=ORDER_STATUS, default='UNPAID', verbose_name='订单状态')
    express_number = models.CharField(max_length=64, blank=True, null=True, verbose_name='快递单号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间') 
    class Meta:
        db_table = 'tb_orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
    
    def save(self, *args, **kwargs):
        # 自动生成订单编号
        if not self.order_number:
            self.order_number = f'ORD{uuid.uuid4().hex[:16].upper()}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    """订单项模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单', related_name='items')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    price = models.DecimalField('商品单价', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('购买数量')
    amount = models.DecimalField('小计金额', max_digits=10, decimal_places=2)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'tb_order_items'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
    
    def __str__(self):
        return f'{self.order.order_number} - {self.goods.name}'
