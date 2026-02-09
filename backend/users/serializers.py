from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=8, error_messages={
        'min_length': '密码长度不能少于8位'
    })
    password_confirm = serializers.CharField(write_only=True, label='确认密码')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'phone', 'email']
        extra_kwargs = {
            'email': {'required': False}
        }

    def validate(self, attrs):
        # 验证两次密码一致
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('两次密码输入不一致')
        # 移除确认密码字段
        attrs.pop('password_confirm')
        return attrs

    def create(self, validated_data):
        # 密码加密
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']