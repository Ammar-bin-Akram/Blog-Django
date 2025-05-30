from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    created_at = models.DateField()


    def __str__(self):
        return self.username
    

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
