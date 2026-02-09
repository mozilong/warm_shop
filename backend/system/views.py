from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import OperationLog, ErrorLog
from .serializers import OperationLogSerializer, ErrorLogSerializer

class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """操作日志视图集"""
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'module', 'operate_type']
    search_fields = ['content', 'operate_ip']
    ordering_fields = ['operate_time']

class ErrorLogViewSet(viewsets.ReadOnlyModelViewSet):
    """错误日志视图集"""
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request_method', 'ip']
    search_fields = ['error_msg', 'request_url']
    ordering_fields = ['error_time']