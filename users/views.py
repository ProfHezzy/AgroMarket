from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # Try to authenticate with username
            user = authenticate(request, username=username, password=password)
            
            # If that fails, try with email
            if user is None:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username/email or password.')
        else:
            messages.error(request, 'Please enter both username/email and password.')
    
    return render(request, 'users/login.html')

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if not all([username, email, password1, password2]):
            messages.error(request, 'Please fill in all required fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
        else:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name or '',
                    last_name=last_name or ''
                )
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('users:login')
    
    return render(request, 'users/register.html')

def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('core:home')

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'users/profile/view.html', {
        'user': request.user
    })

@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        # Handle profile update logic here
        pass
    return render(request, 'users/profile/edit.html')

@login_required
def change_password(request):
    """Change user password"""
    return HttpResponse("<h1>Change Password</h1><p>Password change functionality.</p>")