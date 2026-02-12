from django.http import HttpResponseForbidden
from django.shortcuts import render

class RestrictAdminAccessMiddleware:
    """分级权限控制中间件（极简版）"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 仅拦截已登录用户的Admin请求
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            role = request.user.role
            # 超级管理员：无限制
            if role == 'super_admin':
                pass
            # 普通管理员：可访问用户管理（商户/普通用户）、商品列表（仅下架）
            elif role == 'admin':
                # 禁止管理员添加/编辑超级管理员
                if '/admin/users/user/add/' in request.path or (
                    '/admin/users/user/change/' in request.path and 'role' in request.POST and request.POST['role'] == 'super_admin'
                ):
                    return render(request, '403.html', status=403)
                # 允许管理员访问商品列表/下架商品，禁止新增/编辑商品
                if '/admin/goods/goods/add/' in request.path:
                    return render(request, '403.html', status=403)
            # 商户：仅可访问商品管理（自己的商品），禁止访问用户管理
            elif role == 'merchant':
                if '/admin/users/' in request.path:
                    return render(request, '403.html', status=403)
                # 商户仅可编辑自己的商品
                if '/admin/goods/goods/change/' in request.path and not self.is_own_goods(request):
                    return render(request, '403.html', status=403)
            # 普通用户：禁止访问Admin
            elif role == 'user':
                return render(request, '403.html', status=403)
        
        response = self.get_response(request)
        return response

    def is_own_goods(self, request):
        """判断是否是商户自己的商品"""
        try:
            from goods.models import Goods
            goods_id = request.path.split('/')[-2]
            goods = Goods.objects.get(id=goods_id)
            return goods.merchant == request.user
        except:
            return False
