from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
	
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
	 
	    
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email is already registered.')
        return email
	
	  
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already in use.')
        return username
        
                
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user
        


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
        
        
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already in use.')
        
        
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email is already in use.')       
