from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm
from users.models import User
import re


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен быть не менее 8 символов.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Пароль должен содержать минимум 1 символ верхнего регистра.")
        if not re.search(r'[$%&!:]', password):
            raise forms.ValidationError("Пароль должен содержать минимум 1 спец символ ($%&!:).")
        if not re.match(r'^[a-zA-Z0-9$%&!:]*$', password):
            raise forms.ValidationError("Пароль должен содержать только латиницу и допустимые спецсимволы ($%&!:).")
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError("Телефон должен начинаться с +7, после чего должно идти 10 цифр.")
        return phone

class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['phone', 'password']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError("Телефон должен начинаться с +7, после чего должно идти 10 цифр.")
        return phone

        self.fields['password'].widget = forms.HiddenInput

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email',
                             max_length=254,
                             widget=forms.EmailInput(attrs={
                                 'autocomplete': 'email',
                                 'class': 'form-control',
                                 'placeholder': 'Введите ваш email'}))