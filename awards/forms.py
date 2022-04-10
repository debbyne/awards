from django.forms import ModelForm
from .models import Project,Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=300, help_text='Enter a valid email address')
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput,required=True)

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
        ]

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email',
            'password', 
        ]
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'image',
            'caption'
        ]
