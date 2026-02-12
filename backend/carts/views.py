from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carts.models import Cart
from goods.models import Goods

@login_required
def cart_add(request, goods_id):
    """添加商品到购物车"""
    goods = get_object_or_404(Goods, id=goods_id, status='ON_SALE')
    # 检查库存
    if goods.stock <= 0:
        messages.error(request, '该商品已售罄！')
        return redirect('goods_detail', goods_id=goods_id)
    
    # 检查是否已在购物车
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        goods=goods,
        defaults={'quantity': 1}
    )
    if not created:
        # 已存在则数量+1
        cart_item.quantity += 1
        # 不超过库存
        if cart_item.quantity > goods.stock:
            cart_item.quantity = goods.stock
            messages.warning(request, f'购物车数量已达库存上限（{goods.stock}件）！')
        cart_item.save()
    
    messages.success(request, '商品已加入购物车！')
    return redirect('cart_list')

@login_required
def cart_list(request):
    """购物车列表：编辑/删除"""
    cart_items = Cart.objects.filter(user=request.user)
    # 计算总价
    total_price = sum(item.goods.price * item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': GoodsCategory.objects.all()
    })

@login_required
def cart_delete(request, cart_id):
    """删除购物车商品"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, '已移除该商品！')
    return redirect('cart_list')

@login_required
def cart_update(request, cart_id):
    """更新购物车商品数量"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        # 验证数量
        if quantity < 1:
            quantity = 1
        elif quantity > cart_item.goods.stock:
            quantity = cart_item.goods.stock
            messages.warning(request, f'数量已达库存上限（{cart_item.goods.stock}件）！')
        
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, '购物车已更新！')
    
    return redirect('cart_list')
