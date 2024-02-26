from django.urls import path,include
from foodNet_app import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('feed/', views.feed, name="feed"),
    path('login/', views.signin, name="login"),
    path('profile/', views.profile, name="profile"),
    path('settings/', views.settings, name="settings"),
    path('fooddetails/', views.fooddetails, name="fooddetails"),
]