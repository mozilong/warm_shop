from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from goods.models import Goods
from carts.models import Cart

# 订单创建视图
@login_required
def order_create(request):
    """从购物车创建订单"""
    # 获取当前用户的购物车
    cart_items = Cart.objects.filter(user=request.user, is_active=True)
    if not cart_items.exists():
        messages.error(request, '购物车为空，无法创建订单！')
        return redirect('cart_list')
    
    # 创建订单
    order = Order.objects.create(
        user=request.user,
        total_amount=0,  # 先初始化，后续计算
        status='PENDING'  # 待支付
    )
    
    total_amount = 0
    # 创建订单项
    for cart_item in cart_items:
        goods = cart_item.goods
        # 检查商品库存
        if goods.stock < cart_item.quantity:
            messages.error(request, f'商品「{goods.name}」库存不足！')
            order.delete()  # 删除未完成订单
            return redirect('cart_list')
        
        # 创建订单项
        OrderItem.objects.create(
            order=order,
            goods=goods,
            price=goods.price,
            quantity=cart_item.quantity,
            amount=goods.price * cart_item.quantity
        )
        total_amount += goods.price * cart_item.quantity
        
        # 扣减商品库存
        goods.stock -= cart_item.quantity
        if goods.stock <= 0:
            goods.status = 'OFF_SALE'
        goods.save()
        
        # 标记购物车为已使用
        cart_item.is_active = False
        cart_item.save()
    
    # 更新订单总金额
    order.total_amount = total_amount
    order.save()
    
    messages.success(request, f'订单创建成功！订单编号：{order.order_number}')
    return redirect('order_list')

# 订单列表视图
@login_required
def order_list(request):
    """查看当前用户的所有订单"""
    orders = Order.objects.filter(user=request.user).order_by('-create_time')
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

# 订单物流信息视图
@login_required
def order_express(request, order_id):
    """查看/更新订单物流信息（仅管理员/超级管理员可更新）"""
    order = get_object_or_404(Order, id=order_id)
    
    # 权限校验：仅订单所属用户可查看，管理员/超级管理员可更新
    if order.user != request.user and request.user.role not in ['admin', 'super_admin']:
        messages.error(request, '无权限操作该订单！')
        return redirect('order_list')
    
    if request.method == 'POST':
        # 管理员/超级管理员可更新物流信息
        if request.user.role in ['admin', 'super_admin']:
            express_company = request.POST.get('express_company')
            express_number = request.POST.get('express_number')
            order.express_company = express_company
            order.express_number = express_number
            order.status = 'SHIPPED'  # 已发货
            order.save()
            messages.success(request, '物流信息更新成功！')
            return redirect('order_express', order_id=order.id)
    
    return render(request, 'orders/order_express.html', {
        'order': order
    })
