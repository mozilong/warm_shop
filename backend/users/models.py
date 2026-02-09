"""自定义用户模型，解决与Django内置User模型的冲突"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    自定义用户模型（继承AbstractUser并扩展字段）
    适配电商场景：新增手机号、头像等字段
    """
    # 扩展核心字段
    phone = models.CharField(
        max_length=11, 
        unique=True, 
        verbose_name=_("手机号"),
        help_text=_("请输入11位手机号码")
    )
    avatar = models.ImageField(
        upload_to="avatars/", 
        null=True, 
        blank=True, 
        verbose_name=_("头像"),
        help_text=_("用户头像，支持jpg/png格式")
    )
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = _("用户")
        verbose_name_plural = _("用户")
        db_table = "tb_users"  # 自定义数据库表名
        swappable = 'AUTH_USER_MODEL'  # 标记为可替换的用户模型

    def __str__(self):
        """后台显示用户名"""
        return self.username

    @property
    def full_name(self):
        """拼接姓名（可选）"""
        return f"{self.last_name}{self.first_name}" if self.last_name or self.first_name else self.username