from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter 
from .views import *

router_v1 = DefaultRouter() 
router_v1.register(r'titles', TitleViewSet, basename='titles') 
router_v1.register(r'genres', GenreViewSet, basename='genres') 
router_v1.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router_v1.urls)), 
]