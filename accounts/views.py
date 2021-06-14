from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomUserCreationForm, ProfileForm


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Bad username or password')
    return render(request, 'accounts/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


def user_registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration was successful',
                             extra_tags='alert alert-success alert-dismissible fade show'  # noqa: E501
                            )
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def edit_profile(request):
    form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated ',
                             extra_tags='alert alert-success alert-dismissible fade show'  # noqa: E501
                            )
            return HttpResponseRedirect(reverse('profile', args=[str(request.user.username)]))  # noqa: E501

    return render(request, 'accounts/edit_profile.html', {'form': form})
