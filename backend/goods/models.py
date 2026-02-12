from django.db import models
from users.models import User

# 商品分类模型
class GoodsCategory(models.Model):
    name = models.CharField('分类名称', max_length=50, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.name

# 商品图片模型（首页展示多图）
class GoodsImage(models.Model):
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='所属商品', related_name='images')
    image = models.ImageField('商品图片', upload_to='goods/main/')  # 上传路径：media/goods/main/
    is_default = models.BooleanField('是否默认图', default=False)  # 首页默认展示的图片
    create_time = models.DateTimeField('上传时间', auto_now_add=True)

    class Meta:
        db_table = 'tb_goods_image'
        verbose_name = '商品主图'
        verbose_name_plural = '商品主图'

    def __str__(self):
        return f'{self.goods.name}的图片'

# 商品核心模型（修正缩进问题）
class Goods(models.Model):
    # ========== 关键：这里必须缩进（4个空格） ==========
    STATUS_CHOICES = (
        ('ON_SALE', '已上架'),
        ('OFF_SALE', '已下架'),
    )
    name = models.CharField('商品名称', max_length=100)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品分类')
    stock = models.IntegerField('库存数量', default=0)
    stock_warning = models.IntegerField('库存预警值', default=10)
    description = models.TextField('商品详情')  # 富文本存储详情（含图片）
    merchant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='所属商户', 
        limit_choices_to={'role': 'merchant'}
    )
    status = models.CharField('商品状态', max_length=10, choices=STATUS_CHOICES, default='OFF_SALE')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name
    
    # 库存状态辅助方法（可选）
    def stock_status(self):
        if self.stock <= 0:
            return '缺货'
        elif self.stock <= self.stock_warning:
            return '预警'
        else:
            return '充足'
    stock_status.short_description = '库存状态'
