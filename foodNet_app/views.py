from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, UserModel
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['name']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                messages.success(request, 'Logged In Succesfully')
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')
        
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.POST.get('profile_pic')
        photo_id = request.POST.get('photo_id')
        DOB = request.POST.get('DOB')
        address = request.POST.get('address')
        is_donor = request.POST.get('is_donor')

        try:
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'register.html', {'error_message': 'Username already exists'})

            is_donor = is_donor.lower() == 'true'

            user = User.objects.create_user(username=name, password=password, email=email)

            userModel = UserModel.objects.create(user=user, user_id=user.id, profile_pic=profile_pic,
                                                  photo_id=photo_id, DOB=DOB, address=address,
                                                  is_donor=is_donor, name=name)
            messages.success(request, 'Succesfully registered! Please Login now')
            return redirect('login')
        
        except IntegrityError as e:
            messages.error(request, 'An error occurred while registering the user')
            return render(request, 'register.html', {'error_message': 'An error occurred while registering the user'})

    else:
        return render(request, 'register.html')