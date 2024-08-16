from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import User, Blog, Likes
import datetime
from django.utils import timezone

# Create your views here

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def home(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blogs/home.html', context)

def landing(request):
    return render(request, 'blogs/landing.html')

def create_post(request, user_id):
    user = User.objects.get(pk=user_id)
    context_create = {'user': user}
    blogs = Blog.objects.all()
    context_home = {'blogs': blogs}
    if request.method == "POST":
        title = request.POST.get('title-post')
        content = request.POST.get('content-post')
        created_at = datetime.datetime.now()
        post = Blog(title=title, content=content, created_at = created_at, user=user)
        post.save()
        return redirect('home')
    else:
        return render(request, 'blogs/create.html', context=context_create)


def read_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {'blog': blog}
    return render(request, 'blogs/read.html', context)


def view_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    blogs = Blog.objects.filter(user=user_id)
    latest_blog = blogs[0]
    for blog in blogs:
        if blog.created_at > latest_blog.created_at:
            latest_blog = blog
    context = {'user': user, 'blogs': blogs, 'latest_blog': latest_blog}
    return render(request, 'blogs/profile.html', context)

def like_post(request, blog_id, user_id):
    blog = Blog.objects.get(pk=blog_id)
    user = User.objects.get(pk=user_id)
    like = Likes(user=user, blog=blog)
    like.save()
    return redirect('home')


def view_your_posts(request, user_id):
    blogs = Blog.objects.filter(user=user_id)
    context = {'blogs': blogs}
    return render(request, 'blogs/user_posts.html', context)


def edit_post(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {'blog': blog}
    if request.method == "POST":
        new_title = request.POST.get('title-post')
        new_content = request.POST.get('content-post')
        blog.title = new_title
        blog.content = new_content
        blog.save()
        return redirect('home')
    else:
        return render(request, 'blogs/edit.html', context)


def delete_post(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {'blog': blog}
    if request.method == "POST":
        blog.delete()
        return redirect('home')
    else:
        return render(request, 'blogs/delete.html', context)

