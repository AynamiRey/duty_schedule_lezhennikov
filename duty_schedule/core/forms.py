from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms.widgets import DateInput

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'})
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('username') or not cleaned_data.get('password'):
            raise forms.ValidationError('Пожалуйста, заполните все поля')
        return cleaned_data

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'middle_name', 'birth_date', 'position', 'rank'
        ]
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'middle_name': 'Отчество',
            'birth_date': 'Дата рождения',
            'position': 'Должность',
            'rank': 'Звание',
        }
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True  # Поле username доступно только для чтения
