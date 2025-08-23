from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import RegisterView, LoginView, ProfileView  # from your earlier auth

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]