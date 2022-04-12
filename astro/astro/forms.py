from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth import get_user_model
from astro.astro.models import *
#from captcha.fields import CaptchaField, CaptchaTextInput

User = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Имя пользователя'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Пароль',
            }
        )
    )
    # captcha = CaptchaField(
#         label='Решите простой пример:',
#         widget=CaptchaTextInput(
#             attrs={
#                 'class': 'input100',
#                 'placeholder': 'Введите ответ',
#             }
#         )
#     )


class Sign_Up_Form(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'class': 'input100', 'placeholder': 'Имя пользователя'}))
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Email',

            }
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Пароль',
            }
        )
    )
    password2 = forms.CharField(
        label='Повторный пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Повторите пароль',
            }
        )
    )
#     captcha = CaptchaField(
#         label='Решите простой пример:',
#         widget=CaptchaTextInput(
#             attrs={
#                 'class': 'input100',
#                 'placeholder': 'Введите ответ',
#             }
#         )
#     )

    class Meta(UserCreationForm):
        model = Users
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Email',

            }
        )
    )


class UserPasswordResetForm(SetPasswordForm):
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Email',

            }
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Пароль',
            }
        )
    )
    password2 = forms.CharField(
        label='Повторный пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Повторите пароль',
            }
        )
    )
