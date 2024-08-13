from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class user(AbstractUser):
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    created_at = models.DateField()


    def __str__(self):
        return self.username