from django.urls import path

from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('home/', views.home, name='home'),
    path('', views.landing, name='landing'),
    path('create/<int:user_id>/', views.create_post, name='create'),
    path('read/<int:blog_id>/<int:user_id>/', views.read_blog, name='read'),
    path('your-profile/<int:user_id>/', views.view_profile, name='your-profile'),
    path('your_posts/<int:user_id>/', views.view_your_posts, name='your_posts'),
    path('edit/<int:blog_id>/', views.edit_post, name='edit'),
    path('delete/<int:blog_id>/', views.delete_post, name='delete'),
    path('like/<int:blog_id>/<int:user_id>/', views.like_post, name='like'),
    path('unlike/<int:user_id>/<int:blog_id>/', views.unlike_post, name='unlike'),
    path('create-post/<int:user_id>/',views.create_post, name='create_post'),
    path('profile/<int:blog_id>/', views.others_profile, name='profile'),
]