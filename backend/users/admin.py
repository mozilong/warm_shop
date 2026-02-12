# /app/users/admin.py 修复版
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 自定义UserAdmin（仅保留模型中存在的字段）
class CustomUserAdmin(UserAdmin):
    # 列表页显示的字段（仅保留User模型中实际存在的字段）
    list_display = ('id', 'username', 'phone', 'email', 'is_active', 'date_joined')
    # 列表页筛选条件（仅保留模型中存在的字段）
    list_filter = ('is_active', 'is_staff', 'date_joined')
    # 编辑页字段分组（匹配User模型）
    fieldsets = (
        ('基础信息', {'fields': ('username', 'password', 'phone', 'email')}),
        ('权限配置', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('时间信息', {'fields': ('last_login', 'date_joined')}),
    )
    # 添加用户时的字段（仅保留必填/存在的字段）
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone', 'email', 'is_active'),
        }),
    )
    # 搜索字段
    search_fields = ('username', 'phone', 'email')
    # 排序字段
    ordering = ('-date_joined',)

# 注册自定义User模型和Admin配置
admin.site.register(User, CustomUserAdmin)
