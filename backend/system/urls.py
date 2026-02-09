from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OperationLogViewSet, ErrorLogViewSet

router = DefaultRouter()
router.register(r'system/operation-logs', OperationLogViewSet, basename='operation-log')
router.register(r'system/error-logs', ErrorLogViewSet, basename='error-log')

urlpatterns = [
    path('', include(router.urls)),
]