from rest_framework import serializers
from .models import OperationLog, ErrorLog

class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = ['id', 'user', 'user_name', 'module', 'operate_type', 
                  'operate_ip', 'operate_time', 'content']
        read_only_fields = ['id', 'operate_time']

class ErrorLogSerializer(serializers.ModelSerializer):
    """错误日志序列化器"""
    class Meta:
        model = ErrorLog
        fields = ['id', 'error_time', 'error_msg', 'request_url', 
                  'request_method', 'ip', 'user_agent']
        read_only_fields = ['id', 'error_time']