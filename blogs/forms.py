from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
import datetime

class CustomUserCreationForm(UserCreationForm):
    created_at = forms.DateField(disabled=True, initial=datetime.date.today, label='Created At')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'created_at')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
