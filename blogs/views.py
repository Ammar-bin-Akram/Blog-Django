from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import User, Blog

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
    context = {'user': user}
    return render(request, 'blogs/create.html', context)


def read_blog(request, blog_id):
    return HttpResponse('Read Blog')

