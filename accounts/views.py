from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, SignInForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('user_profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Signed in successfully!")
            return redirect('user_profile')
    else:
        form = SignInForm()
    return render(request, 'accounts/signin.html', {'form': form})


def signout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('signin')


@login_required
def user_profile_view(request):
    return render(request, 'accounts/profile.html')
