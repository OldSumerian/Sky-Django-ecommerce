from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import HiddenInput

from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        labels = {
            'email': 'Адрес электронной почты',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'email': 'Введите адрес электронной почты.',
            'password1': 'Введите пароль.',
            'password2': 'Подтвердите пароль.',
        }


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class UserLoginForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'Адрес электронной почты',
            'password': 'Пароль',
        }
        help_texts = {
            'email': 'Введите адрес электронной почты.',
            'password': 'Введите пароль.',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfilePasswordRestoreForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()

    def clean(self):
        # Намеренная заглушка, чтобы clean-метод не ругался на существующий адрес
        pass

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким адресом электронной почты не найден.')
        return email


