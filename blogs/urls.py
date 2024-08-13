from django.urls import path

from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('home/', views.home, name='home'),
    path('', views.landing, name='landing'),
    path('create/<int:user_id>/', views.create_post, name='create'),
    path('read/<int:blog_id>/', views.read_blog, name='read'),
]