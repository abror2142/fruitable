from .models import Rating
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['user', 'rating', 'product']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'passwordA'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'passwordB'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']