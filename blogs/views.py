from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import User, Blog, Likes, Followers
import datetime
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages

# Create your views here

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def home(request):
    blogs = Blog.objects.annotate(num_likes=Count("likes"))
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


def read_blog(request, blog_id, user_id):
    blog = Blog.objects.get(pk=blog_id)
    user_liked = Likes.objects.filter(blog_id=blog_id, user_id=user_id).exists()
    context = {'blog': blog, 'user_liked': user_liked}
    return render(request, 'blogs/read.html', context)


def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=user_id)
    total_likes = Likes.objects.filter(user=user).count()
    followers = Followers.objects.filter(user=user).count()
    following = Followers.objects.filter(follower=user).count()
    latest_blog = blogs[0]
    for blog in blogs:
        if blog.created_at > latest_blog.created_at:
            latest_blog = blog
    context = {'user': user, 'blogs': blogs, 'latest_blog': latest_blog, 'total_likes': total_likes, 'followers': followers, 'following': following}
    return render(request, 'blogs/profile.html', context)


def like_post(request, blog_id, user_id):
    blogId = user_id
    userId = blog_id
    blog = Blog.objects.get(pk=blogId)
    user = User.objects.get(pk=userId)
    like = Likes(blog=blog, user=user)
    like.save()
    return redirect('home')


def unlike_post(request, user_id, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    user = User.objects.get(pk=user_id)
    like = Likes.objects.get(blog=blog, user=user)
    like.delete()
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


def others_profile(request, blog_id, user_id):
    blog = Blog.objects.get(pk=blog_id)
    logged_in_user = User.objects.get(pk=user_id)
    other_user = blog.user # user whose profile is being viewed
    blogs_user = Blog.objects.filter(user=other_user)
    total_likes = Likes.objects.filter(user=other_user).count()
    user_followers = Followers.objects.filter(user=other_user).count()
    user_following = Followers.objects.filter(follower=other_user).count()
    follows = Followers.objects.filter(follower=logged_in_user, user=other_user).exists()
    latest_blog = blogs_user[0]
    for blog in blogs_user:
        if blog.created_at > latest_blog.created_at:
            latest_blog = blog
    context = {'other_user': other_user, 'blogs': blogs_user, 'latest_blog': latest_blog, 'total_likes': total_likes, 'followers': user_followers, 'following': user_following, 'follows': follows}
    return render(request, 'blogs/others_profile.html', context)


def follow_user(request, follower_id, user_id):
    followed_user = User.objects.get(pk=user_id)
    follower = User.objects.get(pk=follower_id)
    follow_object = Followers(follower=follower, user=followed_user)
    follow_object.save()
    messages.success(request, f'You followed {followed_user.username}')
    return redirect('home')


def unfollow_user(request, follower_id, user_id):
    followed_user = User.objects.get(pk=user_id)
    follower = User.objects.get(pk=follower_id)
    follow_object = Followers.objects.get(follower=follower, user=followed_user)
    print(follow_object.follower)
    print(follow_object.user)
    follow_object.delete()
    messages.warning(request, f'You unfollowed {followed_user.username}')
    return redirect('home')