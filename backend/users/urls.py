from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterViewSet, UserViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users/register', UserRegisterViewSet, basename='user-register')
router.register(r'users/me', UserViewSet, basename='user-me')

urlpatterns = [
    path('', include(router.urls)),
    # JWT登录
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]