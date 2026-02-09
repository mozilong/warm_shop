from django.db import models

class Category(models.Model):
    """商品分类模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='父分类')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'

    def __str__(self):
        return self.name

class Tag(models.Model):
    """商品标签模型"""
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_tag'
        verbose_name = '商品标签'
        verbose_name_plural = '商品标签'

    def __str__(self):
        return self.name

class Goods(models.Model):
    """商品模型"""
    name = models.CharField(max_length=200, verbose_name='商品名称')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods', verbose_name='商品分类')
    tags = models.ManyToManyField(Tag, related_name='goods', blank=True, verbose_name='商品标签')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    stock = models.IntegerField(default=0, verbose_name='库存数量')
    image = models.ImageField(upload_to='goods/', null=True, blank=True, verbose_name='商品图片')
    description = models.TextField(null=True, blank=True, verbose_name='商品描述')
    sales = models.IntegerField(default=0, verbose_name='销售数量')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']

    def __str__(self):
        return self.name