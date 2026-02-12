from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goods

@login_required
def goods_off_shelf(request, goods_id):
    """商品下架视图（管理员/超级管理员/商户都可执行）"""
    goods = get_object_or_404(Goods, id=goods_id)
    user = request.user

    # 权限校验
    if user.role == 'merchant' and goods.merchant != user:
        messages.error(request, '你只能下架自己的商品！')
        return redirect('admin:goods_goods_changelist')
    elif user.role in ['admin', 'super_admin']:
        pass
    elif user.role != 'merchant':
        messages.error(request, '无权限下架商品！')
        return redirect('admin:goods_goods_changelist')

    # 执行下架
    goods.status = 'OFF_SALE'
    goods.save()
    messages.success(request, f'商品「{goods.name}」已下架！')
    return redirect('admin:goods_goods_changelist')

@login_required
def goods_on_shelf(request, goods_id):
    """商品上架视图（仅商户可执行）"""
    goods = get_object_or_404(Goods, id=goods_id)
    user = request.user

    # 仅商户可上架自己的商品
    if user.role != 'merchant' or goods.merchant != user:
        messages.error(request, '仅商户可上架自己的商品！')
        return redirect('admin:goods_goods_changelist')

    # 执行上架（库存>0才允许）
    if goods.stock <= 0:
        messages.error(request, '库存为0，无法上架商品！')
        return redirect('admin:goods_goods_changelist')
    
    goods.status = 'ON_SALE'
    goods.save()
    messages.success(request, f'商品「{goods.name}」已上架！')
    return redirect('admin:goods_goods_changelist')
