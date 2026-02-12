from django.contrib import admin
from .models import Order

@admin.register(Order)  # 保留装饰器注册方式
class OrderAdmin(admin.ModelAdmin):
    """订单Admin（最终版：修复重复注册+字段匹配）"""
    # 核心：仅保留模型实际存在的字段（需与你的Order模型字段严格一致）
    list_display = [
        'order_number',       # 订单编号（替换原order_sn）
        'user',               # 下单用户
        'goods_item',         # 关联商品（替换原goods）
        'total_amount',       # 订单总价（替换原total_price）
        'status',             # 订单状态
        'express_number',     # 快递单号（替换原express_no）
        'create_time'         # 创建时间
    ]
    
    # 筛选条件（仅保留模型实际存在的关联字段）
    list_filter = [
        'status',             # 订单状态
        'goods_item__merchant'# 商品所属商户（若Goods模型有merchant字段则保留，否则删除）
    ]
    
    # 搜索字段
    search_fields = [
        'order_number',       # 按订单编号搜索
        'user__username',     # 按用户名搜索
        'express_number'      # 按快递单号搜索
    ]
    
    # 字段分组
    fieldsets = (
        ('订单信息', {
            'fields': ('order_number', 'user', 'goods_item', 'price', 'quantity', 'total_amount')
        }),
        ('状态信息', {
            'fields': ('status', 'express_number')
        }),
        ('时间信息', {
            'fields': ('create_time', 'update_time')
        }),
    )
    
    # 只读字段（不允许手动修改）
    readonly_fields = ('create_time', 'update_time')
    
    # 数据过滤：商户仅看自己商品的订单
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'merchant':
            return qs.filter(goods_item__merchant=request.user)
        return qs
    
    # 权限控制
    def has_view_permission(self, request, obj=None):
        return True  # 所有人可查看（按角色过滤数据）
    
    def has_change_permission(self, request, obj=None):
        return request.user.role in ['super_admin', 'admin']  # 仅管理员可修改
    
    def has_delete_permission(self, request, obj=None):
        return request.user.role == 'super_admin'  # 仅超级管理员可删除
    
    def has_add_permission(self, request):
        return False  # 禁止手动新增订单

# ========== 关键：删除以下重复注册代码 ==========
# admin.site.register(Order, OrderAdmin)  # 这行是重复注册的根源，直接删除
