from django.contrib import admin
from .models import Category  # Импортируем модель Category

# Регистрируем модель Category в админке
admin.site.register(Category)