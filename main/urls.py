
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # Регистрация
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Вход
    path('create_request/', views.create_request, name='create_request'),
    path('my_requests/', views.my_requests, name='my_requests'),  # Список заявок
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),  # Страница заявки
    path('request/<int:id>/delete/', views.delete_request, name='delete_request'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
