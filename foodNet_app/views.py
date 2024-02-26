from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, UserModel
# Create your views here.


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def feed(request):
    return render(request, 'feed.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('first_name')
        password = request.POST.get('last_name')
        profile_pic = request.POST.get('last_name')
        photo_id = request.POST.get('last_name')
        DOB = request.POST.get('last_name')
        address = request.POST.get('last_name')
        is_donor = request.POST.get('last_name')
        user = User.objects.create(name=name,
                                    password=password,
                                    )
        userModel = UserModel.objects.create(profile_pic = profile_pic,
                                    photo_id = photo_id,
                                    DOB = DOB,
                                    address = address,
                                    is_donor = is_donor,
                                    user = user)
        userModel.save()
        user.save()
        
        return redirect('index')
    else:
        return render(request, 'register.html')

