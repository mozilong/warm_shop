"""注册自定义用户模型到Django后台，支持后台管理"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

# 自定义UserAdmin配置（适配扩展字段）
class CustomUserAdmin(UserAdmin):
    """自定义用户后台显示配置"""
    # 列表页显示字段
    list_display = ('username', 'phone', 'email', 'is_staff', 'is_active', 'created_at')
    # 列表页筛选条件
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    # 搜索字段
    search_fields = ('username', 'phone', 'email')
    # 详情页字段分组
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    # 新增用户时的字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    # 只读字段
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    # 默认排序
    ordering = ('-created_at',)

# 注册自定义用户模型
admin.site.register(User, CustomUserAdmin)