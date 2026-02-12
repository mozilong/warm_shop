from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# 获取自定义User模型
User = get_user_model()

class RegisterForm(forms.ModelForm):
    """用户注册表单"""
    # 新增确认密码字段
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'placeholder': '再次输入密码'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '用户名'}),
            'phone': forms.TextInput(attrs={'placeholder': '手机号'}),
            'password': forms.PasswordInput(attrs={'placeholder': '密码'}),
        }
        labels = {
            'username': '用户名',
            'phone': '手机号',
            'password': '密码',
        }

    # 验证密码一致性
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            raise forms.ValidationError('两次输入的密码不一致！')
        return cleaned_data

    # 验证密码强度
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # 使用Django内置密码验证
        return password

    # 保存用户（加密密码）
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # 加密密码
        # 默认注册为普通用户
        if not hasattr(user, 'role') or user.role is None:
            user.role = 'user'
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    """用户登录表单"""
    username = forms.CharField(
        label='用户名/手机号',
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名或手机号'}),
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
        required=True
    )

    # 验证用户名/手机号是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 检查是用户名还是手机号
        if not User.objects.filter(username=username).exists() and not User.objects.filter(phone=username).exists():
            raise forms.ValidationError('用户名或手机号不存在！')
        return username
