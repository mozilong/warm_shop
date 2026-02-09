"""商品基础模型，定义商品核心字段"""
from django.db import models
from django.utils.translation import gettext_lazy as _

class Goods(models.Model):
    """
    商品基础模型
    包含名称、价格、库存、图片等核心字段
    """
    # 商品状态枚举
    class GoodsStatus(models.TextChoices):
        ON_SALE = 'ON_SALE', _('在售')
        OFF_SALE = 'OFF_SALE', _('下架')
        OUT_OF_STOCK = 'OUT_OF_STOCK', _('缺货')

    # 核心字段
    name = models.CharField(
        max_length=200, 
        verbose_name=_("商品名称"),
        help_text=_("商品名称，最长200字符")
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_("商品价格"),
        help_text=_("商品售价，保留2位小数")
    )
    stock = models.IntegerField(
        default=0, 
        verbose_name=_("库存数量"),
        help_text=_("商品库存数量，非负整数")
    )
    status = models.CharField(
        max_length=20,
        choices=GoodsStatus.choices,
        default=GoodsStatus.ON_SALE,
        verbose_name=_("商品状态")
    )
    image = models.ImageField(
        upload_to="goods/",
        null=True,
        blank=True,
        verbose_name=_("商品图片"),
        help_text=_("商品主图，支持jpg/png格式")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("商品描述"),
        help_text=_("商品详细介绍")
    )
    # 时间字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = _("商品")
        verbose_name_plural = _("商品")
        db_table = "tb_goods"
        ordering = ["-create_time"]  # 默认按创建时间降序排列

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        """判断是否有库存"""
        return self.stock > 0 and self.status == self.GoodsStatus.ON_SALE