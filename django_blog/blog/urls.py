from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
# Home (optional — can show links)
path('', views.home, name='home'),


# Auth
path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('register/', views.register, name='register'),

# Profile
path('profile/', views.profile, name='profile'),
path('profile/edit/', views.profile_edit, name='profile_edit'),
]