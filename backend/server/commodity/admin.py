from django.contrib import admin
from .models import *

# admin.site.register(Types)
# admin.site.register(CommodityInfos)

# 修改title和header
admin.site.site_title = '蓝云飞飞后台系统'
admin.site.site_header = '蓝云飞飞电商后台管理系统'
admin.site.index_title = '蓝云飞飞平台管理'

@admin.register(Types)
class TypesAdmin(admin.ModelAdmin):
    list_display = [x for x in list(Types._meta._forward_fields_map.keys())]
    search_fields = ['firsts', 'seconds']
    list_filter = ['firsts']
    list_editable = ['firsts', 'seconds']

# @admin.register(CommodityInfos)
# class CommodityInfosAdmin(admin.ModelAdmin):
#     list_display = [x for x in list(CommodityInfos._meta._forward_fields_map.keys())]
#     search_fields = ['name']
#     date_hierarchy = 'created'
#
#     def formfield_for_dbfield(self, db_field, **kwargs):
#         if db_field.name == 'types':
#             db_field.choices = [(x['seconds'], x['seconds'])for x in Types.objects.values('seconds')]
#         return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(CommodityInfos)
class CommodityInfosAdmin(admin.ModelAdmin):
    # 改变数据新增页或数据修改页的网页布局
    fieldsets = (
        ('商品信息', {
            'fields': ('name','sezes','types','price','discount','stock','sold','img','details')
        }),
        ('收藏数量', {
            # 设置隐藏与显示
            'classes': ('collapse',),
            'fields': ('likes',),
        }),
    )

    # 将下拉框改为单选按钮
    # admin.HORIZONTAL是水平排列
    # admin.VERTICAL是垂直排列
    # radio_fields = {'types': admin.HORIZONTAL}

    # 在数据新增页或数据修改页设置可读的字段，不可编辑
    # readonly_fields = ['sold',]

    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']

    # 设置数据列表页的每列数据是否可排序显示
    sortable_by = ['price', 'discount']

    # 在数据列表页设置显示的模型字段
    list_display = ['id', 'name', 'sezes', 'types', 'price', 'discount','img','details']
    list_display.append('colored_name')

    # 为数据列表页的字段id和name设置路由地址，该路由地址可进入数据修改页
    # list_display_links = ['id', 'name']

    # 设置过滤器，若有外键，则应使用双下画线连接两个模型的字段
    list_filter = ['types']

    # 在数据列表页设置每一页显示的数据量
    list_per_page = 100

    # 在数据列表页设置每一页显示最大上限的数据量
    list_max_show_all = 200

    # 为数据列表页的字段name设置编辑状态
    list_editable = ['name','sezes','types','price','discount','img','details']

    # 设置可搜索的字段
    search_fields = ['name', 'types']

    # 在数据列表页设置日期选择器
    date_hierarchy = 'created'

    # 在数据修改页添加“另存为”功能
    save_as = True

    # 设置“动作”栏的位置
    # actions_on_top = False
    # actions_on_bottom = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'types':
            db_field.choices = [(x['seconds'], x['seconds'])for x in Types.objects.values('seconds')]
        return super().formfield_for_dbfield(db_field, **kwargs)

