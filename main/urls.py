
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # Регистрация
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Вход
]
