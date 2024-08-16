from django.urls import path

from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('home/', views.home, name='home'),
    path('', views.landing, name='landing'),
    path('create/<int:user_id>/', views.create_post, name='create'),
    path('read/<int:blog_id>/', views.read_blog, name='read'),
    path('profile/<int:user_id>/', views.view_profile, name='profile'),
    path('your_posts/<int:user_id>/', views.view_your_posts, name='your_posts'),
    path('edit/<int:blog_id>/', views.edit_post, name='edit'),
    path('delete/<int:blog_id>/', views.delete_post, name='delete'),
    path('like/<int:blog_id>/<int:user_id>/', views.like_post, name='like'),
]