"""首页视图文件，处理根路径访问"""
from django.shortcuts import render


def home(request):
    """
    首页视图
    :param request: HTTP请求对象
    :return: 渲染后的首页模板
    """
    return render(request, 'home.html', {
        'title': '暖心商城',
        'message': '欢迎访问暖心线上商城系统！'
    })