from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
                  label='Username',
                  max_length=100,
                  min_length=5,
                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
                  label="Password",
                  max_length=100,
                  min_length=5,
                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
                  label="Confirm Password",
                  max_length=100,
                  min_length=5,
                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):

    username = forms.CharField(
                  label='Username',
                  max_length=100,
                  min_length=5,
                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', ]
