from django.urls import path,include
from foodNet_app import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feed/', views.feed, name="feed"),
    path('login/', views.signin, name="login"),
    path('profile/', views.profile, name="profile"),
    path('settings/', views.settings, name="settings"),
    path('fooddetails/', views.fooddetails, name="fooddetails"),
    path('logout/', views.signout, name='logout'),
    path('switch_role/<str:name>/', views.switch_role, name='switch_role'),
    path('get_user_data/<str:name>/', views.get_user_data, name='get_user_data'),
    path('create_food/', views.create_food, name='create_food'),
    path('accept_food/<int:food_id>/', views.accept_food, name='accept_food'),
    path('delete_food/<int:food_id>/', views.delete_food, name='delete_food'),
]