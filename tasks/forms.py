from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegistrationForms(UserCreationForm):
    class Meta:
        models = User
        fields=['username','email','password1', 'password2']