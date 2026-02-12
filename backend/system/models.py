from django.db import models
from users.models import User

class OperationLog(models.Model):
    """操作日志模型"""
    OPERATE_TYPE = (
        ('login', '登录'),
        ('logout', '登出'),
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
        ('query', '查询'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='操作用户')
    module = models.CharField(max_length=50, verbose_name='操作模块')
    operate_type = models.CharField(max_length=20, choices=OPERATE_TYPE, verbose_name='操作类型')
    operate_ip = models.CharField(max_length=45, verbose_name='操作IP')
    operate_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    content = models.TextField(null=True, blank=True, verbose_name='操作内容')

    class Meta:
        db_table = 'tb_operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        ordering = ['-operate_time']

    def __str__(self):
        return f'{self.user.username if self.user else "匿名"} - {self.module} - {self.operate_type}'

class ErrorLog(models.Model):
    """错误日志模型"""
    error_time = models.DateTimeField(auto_now_add=True, verbose_name='错误时间')
    error_msg = models.TextField(verbose_name='错误信息')
    request_url = models.CharField(max_length=255, verbose_name='请求URL')
    request_method = models.CharField(max_length=10, verbose_name='请求方法')
    ip = models.CharField(max_length=45, verbose_name='IP地址')
    user_agent = models.TextField(null=True, blank=True, verbose_name='用户代理')

    class Meta:
        db_table = 'tb_error_logs'
        verbose_name = '错误日志'
        verbose_name_plural = '错误日志'
        ordering = ['-error_time']

    def __str__(self):
        return f'{self.error_time} - {self.request_url}'