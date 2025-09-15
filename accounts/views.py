
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

# Create your views here.
def register(request):
    """Register a new user and log them in immediately."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, 'Welcome — your account has been created.')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})




@login_required
def profile(request):
    """Simple profile page showing username and email."""
    return render(request, 'accounts/profile.html')

@login_required
def account_view(request):
    return render(request, 'accounts/account.html')