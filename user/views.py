from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound, HttpResponse #(path of the page)
from django.urls import reverse #(name of the url,args=[redirect_month]
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Profile
import os

def test(request):
    return HttpResponseNotFound("Page not found")

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Logged in successfully")
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def next_register_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        city = request.POST['city']
        governorate = request.POST['governorate']
        profile_picture = request.POST['profile_picture']
        user = request.user
        Profile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            city=city,
            governorate=governorate,
            profile_picture=profile_picture,
        )
        return redirect('login')
        
    return render(request, 'user/next_register_page.html')

def profile_view(request):
    return render(request, 'user/profile.html')

def profile_update_view(request):
    if request.method == 'POST':
        # Update user fields if provided
        if 'first_name' in request.POST:
            request.user.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            request.user.last_name = request.POST['last_name']
        if 'email' in request.POST:
            request.user.email = request.POST['email']
        request.user.save()
        
        # Get the current user's profile
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None
        
        if not profile:
            Profile.objects.create(
                user=request.user,
                phone_number=request.POST['phone_number'],
                address=request.POST['address'],
                city=request.POST['city'],
                governorate=request.POST['governorate'],
                profile_picture=request.FILES['profile_picture'],
            )
            return redirect('profile')
        
        # Update profile fields if provided
        if 'phone_number' in request.POST:
            profile.phone_number = request.POST['phone_number']
        if 'address' in request.POST:
            profile.address = request.POST['address']
        if 'city' in request.POST:
            profile.city = request.POST['city']
        if 'governorate' in request.POST:
            profile.governorate = request.POST['governorate']
        
        # Handle profile picture update
        if 'profile_picture' in request.FILES:
            # Delete old profile picture if it exists
            if profile.profile_picture:
                # Get the path to the old image
                old_image_path = profile.profile_picture.path
                # Delete the file from storage
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
            # Set the new profile picture
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'user/profile_edit.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1'] 
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'user/register.html')

        try:
            User = get_user_model()
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
            )
            login(request, user)
            return redirect('next_register')
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'user/register.html')

    return render(request, 'user/register.html')


