from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='design_requests')  # Связь с пользователем
    title = models.CharField(max_length=200)  # Название заявки
    description = models.TextField()  # Описание заявки
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Категория
    photo = models.ImageField(upload_to='design_photos/', null=True, blank=True)  # Фото помещения
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заявки
    is_completed = models.BooleanField(default=False)  # Статус выполнения заявки

    def __str__(self):
        return f'Заявка от {self.user.username} на {self.title}'

    def clean(self):
        # Валидация размера изображения
        if self.photo:
            file_size = self.photo.size
            if file_size > 2 * 1024 * 1024:  # 2MB
                raise ValidationError("Размер изображения не должен превышать 2MB.")

            # Проверка на разрешенные форматы
            valid_extensions = ['jpg', 'jpeg', 'png', 'bmp']
            ext = self.photo.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Фото должно быть в одном из форматов: jpg, jpeg, png, bmp.")
