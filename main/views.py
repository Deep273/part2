from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DesignRequestForm
from django.shortcuts import render, get_object_or_404
from .models import DesignRequest

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


@login_required  # Эта декорация гарантирует, что заявку может создать только авторизованный пользователь
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user  # Устанавливаем пользователя, подавшего заявку
            design_request.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('home')  # Перенаправляем на главную страницу после создания заявки
        else:
            # Если форма не валидна, выводим ошибки
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = DesignRequestForm()

    return render(request, 'main/create_request.html', {'form': form})


# Страница списка всех заявок пользователя
def my_requests(request):
    # Получаем все заявки текущего пользователя
    requests = DesignRequest.objects.filter(user=request.user)

    return render(request, 'main/my_requests.html', {'requests': requests})

# Страница с подробной информацией о заявке
def request_detail(request, request_id):
    # Получаем заявку по id
    design_request = get_object_or_404(DesignRequest, id=request_id)

    return render(request, 'main/request_detail.html', {'request': design_request})