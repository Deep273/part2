from django.contrib import admin
from .models import Category, DesignRequest


if admin.site.is_registered(Category):
    admin.site.unregister(Category)

# Регистрируем модель Category только один раз
admin.site.register(Category)

class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('user', 'category', 'created_at')
    search_fields = ('title', 'description')

# Регистрируем модель DesignRequest с кастомной настройкой
admin.site.register(DesignRequest, DesignRequestAdmin)