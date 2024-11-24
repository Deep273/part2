from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        min_length=3,
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Введите логин (только латиница и дефис)'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email'}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        min_length=8,
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalnum() and '-' not in username:
            raise ValidationError('Логин может содержать только латинские буквы и дефис.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Этот логин уже занят.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже зарегистрирован.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2