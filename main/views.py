from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout

def home(request):
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        welcome_message = f"Привет, {request.user.username}!"
    else:
        welcome_message = "Привет, гость! Пожалуйста, войдите или зарегистрируйтесь."

    return render(request, 'main/index.html', {'welcome_message': welcome_message})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Создание пользователя
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # Автоматически входим после регистрации
            return redirect('home')  # Перенаправление на главную страницу после регистрации
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Получаем данные и аутентифицируем пользователя
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Авторизуем пользователя
                return redirect('home')  # Перенаправляем на главную страницу
            else:
                form.add_error(None, 'Неверный логин или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправляем на главную страницу после выхода