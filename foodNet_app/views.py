from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, UserModel, Food
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate,login,logout
from django.utils.timezone import make_aware
from datetime import datetime
import json
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.


def index(request):
    return render(request, 'index.html')

@login_required()
def dashboard(request):
    user = get_object_or_404(User, username=request.user.username)

    userDetails = get_object_or_404(UserModel, user=user)

    foods = Food.objects.all()
    context = {
        'user': user,
        'userDetails': userDetails,
        'foods': foods
    }
    return render(request, 'dashboard.html', context)

def feed(request):
    return render(request, 'feed.html')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

def fooddetails(request):
    return render(request, 'fooddetails.html')

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
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')
        
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        DOB = request.POST.get('DOB')
        address = request.POST.get('address')
        is_donor = request.POST.get('is_donor')

        # Get the uploaded files from the FILES attribute
        profile_pic = request.FILES.get('profile_pic')
        photo_id = request.FILES.get('photo_id')

        try:
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'register.html', {'error_message': 'Username already exists'})

            is_donor = is_donor.lower() == 'true'

            user = User.objects.create_user(username=name, password=password, email=email)

            userModel = UserModel.objects.create(user=user, profile_pic=profile_pic, photo_id=photo_id,
                                                  DOB=DOB, address=address, is_donor=is_donor, name=name)
            messages.success(request, 'Successfully registered! Please Login now')
            return redirect('login')
        
        except IntegrityError as e:
            messages.error(request, 'An error occurred while registering the user')
            return render(request, 'register.html', {'error_message': 'An error occurred while registering the user'})

    else:
        return render(request, 'register.html')

@login_required()
def signout(request): 
    logout(request)
    return redirect('login')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def switch_role(request, name):
    if request.method == 'POST':
        try:
            # Retrieve the corresponding UserModel instance
            user_model = get_object_or_404(UserModel, name=name)
            
            # Toggle the is_donor value
            user_model.is_donor = not user_model.is_donor
            
            # Save the changes to the database
            user_model.save()
            
            # Return a success response
            return JsonResponse({'status': 'success', 'is_donor': user_model.is_donor})
        except Exception as e:
            # Handle exceptions such as user not found or database errors
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'GET':
        # Handle GET request to retrieve user data
        user_model = get_object_or_404(UserModel, name=name)
        return JsonResponse({'is_donor': user_model.is_donor})
    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return HttpResponseNotAllowed(['POST', 'GET'])
    

def get_user_data(request, name):
    try:
        # Retrieve user data based on the username
        user = UserModel.objects.get(name=name)
        
        # Example: Retrieve relevant user data and construct JSON response
        user_data = {
            'name': user.name,
            'is_donor': user.is_donor,
        }
        
        # Return user data in JSON format
        return JsonResponse(user_data)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    

from django.utils.timezone import make_aware

def create_food(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        type = request.POST.get('type')
        weight = request.POST.get('weight')
        expiry_date = request.POST.get('expiry_date')
        desc = request.POST.get('desc')
        postal_code = request.POST.get('postal_code')
        cooked_time = request.POST.get('cooked_time')
        
        # Convert cooked_time to datetime object
        cooked_time = make_aware(datetime.strptime(cooked_time, '%Y-%m-%dT%H:%M'))

        # Convert expiry_date to date object
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        
        # Get the current user
        user = request.user

        # Create the Food object
        food = Food.objects.create(
            provider=user,
            image=image,
            type=type,
            weight=weight,
            expiry_date=expiry_date,
            desc=desc,
            postal_code=postal_code,
            cooked_time=cooked_time
        )

        messages.success(request, 'Food added created successfully. Please wait for the receiver to pick up.')
        return redirect('dashboard')
    else:
        return render(request, 'dashboard.html')
    

def generate_unique_code():
    return str(random.randint(1000, 9999))

def accept_food(request, food_id):
    food = Food.objects.get(pk=food_id)
    
    # Update the taker and status fields
    food.taker = request.user
    food.status = False
    
    # Generate a unique 4-digit code
    unique_code = generate_unique_code()
    food.unique_code = unique_code

    food.save()

    host = 'nicebanjaraa@gmail.com'

    provider_subject = 'Your food offer has been accepted!'
    provider_message = render_to_string('email/taker_accept_food_email.html', {'food': food})
    send_mail(provider_subject, provider_message, host, [food.provider.email])

    # Send email notification to the taker
    messages.success(request, 'Please check your mail for more information')
    taker_subject = 'You have successfully accepted a food offer!'
    taker_message = render_to_string('email/taker_accept_food_email.html', {'food': food, 'unique_code': unique_code})
    send_mail(taker_subject, taker_message, host, [request.user.email])

    return redirect('dashboard')


def delete_food(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    if food.provider == request.user:
        messages.success(request, 'Memento deleted successfully.')
        food.delete()
        return redirect('dashboard')
    else:
        messages.error(request, 'Memento deleted successfully.')
        return redirect('dashboard')