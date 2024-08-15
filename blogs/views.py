from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import User, Blog
import datetime

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
        post = Blog(title=title, content=content,created_at = created_at, user=user)
        post.save()
        return redirect('home')
    else:
        return render(request, 'blogs/create.html', context=context_create)


def read_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {'blog': blog}
    return render(request, 'blogs/read.html', context)

