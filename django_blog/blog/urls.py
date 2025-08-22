from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)


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

# Blog Post URLs
path('post/', views.PostListView.as_view(), name='post_list'),
path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
path('post/new/', views.PostCreateView.as_view(), name='post_create'),
path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),path('posts/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]