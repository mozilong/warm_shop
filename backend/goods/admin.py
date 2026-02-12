from django.contrib import admin
from .models import Goods, GoodsCategory, GoodsImage  # 导入多图模型
from ckeditor.widgets import CKEditorWidget  # 富文本编辑器
from django import forms


# ========== 新增：商品详情富文本表单（支持上传详情图） ==========
class GoodsForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorWidget(config_name='default'),  # 富文本编辑器
        label='商品详情'
    )
    class Meta:
        model = Goods
        fields = '__all__'


# ========== 新增：商品多图内联（在商品页面直接上传多图） ==========
class GoodsImageInline(admin.TabularInline):
    model = GoodsImage
    extra = 3  # 默认显示3个上传框
    fields = ['image', 'is_default']  # 上传图片+设置默认图
    verbose_name = '商品主图'
    verbose_name_plural = '商品主图'


# 商品Admin（关联内联+富文本）
@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    form = GoodsForm  # 启用富文本详情
    inlines = [GoodsImageInline]  # 启用多图内联

    # 列表显示字段
    list_display = ['name', 'price', 'category', 'stock', 'merchant', 'status', 'create_time']
    list_filter = ['category', 'merchant', 'status']
    search_fields = ['name']

    # 字段分组（优化添加页面布局）
    fieldsets = (
        ('基础信息', {
            'fields': ('name', 'price', 'category', 'status')
        }),
        ('库存管理', {
            'fields': ('stock', 'stock_warning')
        }),
        ('商品详情', {
            'fields': ('description',)  # 富文本详情
        }),
        ('归属信息', {
            'fields': ('merchant',)
        }),
    )

    # 权限控制（保留原有逻辑）
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'merchant':
            return qs.filter(merchant=request.user)
        return qs

    def has_add_permission(self, request):
        return request.user.role == 'merchant'

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'merchant':
            return obj and obj.merchant == request.user
        return False
