from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
from django import forms

class ResetPasswordForm(SetPasswordForm):
    # Personalizar el formulario aquí si es necesario
    pass

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

class CustomUserUpdateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name','role']