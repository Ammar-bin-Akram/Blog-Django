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

# Views to create the sign up page of website
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# view where the logged in user first comes after log in, it shows all the posts of each user
def home(request):
    blogs = Blog.objects.annotate(num_likes=Count("likes"))
    context = {'blogs': blogs}
    return render(request, 'blogs/home.html', context)

# the landing page of the website
def landing(request):
    return render(request, 'blogs/landing.html')

# view that renders the form to create a post, it takes in user id as an argument and then checks if the form is filled or not, if filled it 
# saves the post, if not it renders the create post page 
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
        messages.success(request, f"Your post {title} has been posted.")
        return redirect('home')
    else:
        return render(request, 'blogs/create.html', context=context_create)


# view that renders the blog that the logged in user wants to read, it takes in user id and blog id as an argument
def read_blog(request, blog_id, user_id):
    blog = Blog.objects.get(pk=blog_id)
    user_liked = Likes.objects.filter(blog_id=blog_id, user_id=user_id).exists()
    context = {'blog': blog, 'user_liked': user_liked}
    return render(request, 'blogs/read.html', context)


# view that renders the profile page of the logged in user, it takes in user id as an argument
def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(user=user_id)
    total_likes = Likes.objects.filter(user=user).count() # likes that the user has received
    followers = Followers.objects.filter(user=user).count() # followers of the user
    following = Followers.objects.filter(follower=user).count() # users that the user is following
    latest_blog = blogs[0] # the line and for loop is to find the latest blog of the user
    for blog in blogs:
        if blog.created_at > latest_blog.created_at:
            latest_blog = blog
    # context variables that are passed to the template
    context = {'user': user, 'blogs': blogs, 'latest_blog': latest_blog, 'total_likes': total_likes, 'followers': followers, 'following': following} 
    return render(request, 'blogs/profile.html', context)


# view for liking a post, it takes user id and blog id as argument
def like_post(request, blog_id, user_id):
    blogId = user_id
    userId = blog_id
    blog = Blog.objects.get(pk=blogId)
    user = User.objects.get(pk=userId)
    like = Likes(blog=blog, user=user) # like object is created 
    like.save() # like object is saved in db
    messages.success(request, f"You liked {blog.user.username}'s {blog.title} ") # message that will be shown after the post is liked
    return redirect('home')


# view for unliking a post, it takes user id and blog id as an argument
def unlike_post(request, user_id, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    user = User.objects.get(pk=user_id)
    like = Likes.objects.get(blog=blog, user=user) # like object is fetched form db
    like.delete() # like object deleted
    messages.warning(request, f"You unliked {blog.user.username}'s post {blog.title} ")
    return redirect('home')


# view to show the logged in user all his posts, it takes user id as an argument
def view_your_posts(request, user_id):
    blogs = Blog.objects.filter(user=user_id)
    context = {'blogs': blogs}
    return render(request, 'blogs/user_posts.html', context)


# view to edit a post, it takes blog id as an argument, checks if the form is filled, if yes then, saves the edited post, if not then 
# renders the edit page
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


# view to delete a post, it takes blog id as an argument, checks if the method is post, if yes then deletes the post, else render the delete page
def delete_post(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {'blog': blog}
    if request.method == "POST":
        blog.delete()
        messages.warning(request, f"Your post {blog.title} has been deleted. ")
        return redirect('home')
    else:
        return render(request, 'blogs/delete.html', context)


# view to show the profile of other users, it takes blog id, user id as an argument
def others_profile(request, blog_id, user_id):
    blog = Blog.objects.get(pk=blog_id) 
    logged_in_user = User.objects.get(pk=user_id) # user that is logged in
    other_user = blog.user # user whose profile is being viewed
    blogs_user = Blog.objects.filter(user=other_user) # all posts of the user whose profile is being viewed
    total_likes = Likes.objects.filter(user=other_user).count() # all likes of the user whose profile is being viewed
    user_followers = Followers.objects.filter(user=other_user).count() # all followers of the user whose profile is being viewed
    user_following = Followers.objects.filter(follower=other_user).count() # all following of the user whose profile is being viewed
    follows = Followers.objects.filter(follower=logged_in_user, user=other_user).exists() # checks if the logged in user follows the other user or not
    latest_blog = blogs_user[0] # this line and for loop is to find the latest blog of the user whose profile is being viewed
    for blog in blogs_user:
        if blog.created_at > latest_blog.created_at:
            latest_blog = blog
    # context variables being passed to the template
    context = {'other_user': other_user, 'blogs': blogs_user, 'latest_blog': latest_blog, 'total_likes': total_likes, 'followers': user_followers, 'following': user_following, 'follows': follows}
    return render(request, 'blogs/others_profile.html', context)


# view to follow any user, it takes follower id, user id as an argument, user id refers to the user that is being followed, follower id is the 
# id of the user who is following
def follow_user(request, follower_id, user_id):
    followed_user = User.objects.get(pk=user_id)
    follower = User.objects.get(pk=follower_id)
    follow_object = Followers(follower=follower, user=followed_user)
    follow_object.save()
    messages.success(request, f'You followed {followed_user.username}')
    return redirect('home')

# view to unfollow any user, it takes follower id, user id as an argument, user id refers to the user that is being followed, follower id is the 
# id of the user who is following
def unfollow_user(request, follower_id, user_id):
    followed_user = User.objects.get(pk=user_id)
    follower = User.objects.get(pk=follower_id)
    follow_object = Followers.objects.get(follower=follower, user=followed_user)
    follow_object.delete()
    messages.warning(request, f'You unfollowed {followed_user.username}')
    return redirect('home')