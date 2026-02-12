from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(
        max_length=11, 
        blank=True,  # 允许为空
        null=True,   # 数据库允许NULL
        unique=True, # 仅手机号设为唯一
        verbose_name="手机号"
    )
    # 关键：确保email字段取消唯一约束（Django默认AbstractUser的email是unique=True，需显式覆盖）
    email = models.EmailField(
        blank=True,
        null=True,
        unique=False,  # 取消email唯一约束（核心修复！）
        verbose_name="邮箱"
    )

    class Meta:
        db_table = "users_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
