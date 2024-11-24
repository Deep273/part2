
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),  # Вход
]
