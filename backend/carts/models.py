from django.db import models
from users.models import User
from goods.models import Goods  # 确认导入路径和模型名正确

class Cart(models.Model):
    """购物车模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='关联商品')
    count = models.IntegerField(default=1, verbose_name='商品数量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        db_table = 'tb_cart'
        unique_together = ('user', 'goods')  # 一个用户一个商品只能有一条购物车记录
    
    def __str__(self):
        return f'{self.user.username}的购物车：{self.goods.name} x {self.count}'
    
    # 计算购物车项总价
    @property
    def total_price(self):
        return self.goods.price * self.count
