from django.db import models
from users.models import User
from goods.models import Goods

class Cart(models.Model):
    """购物车模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_carts'
        unique_together = ('user', 'goods')  # 同一用户同一商品唯一
        verbose_name = '购物车'
        verbose_name_plural = '购物车'

    def __str__(self):
        return f'{self.user.username} - {self.goods.name} ({self.quantity})'