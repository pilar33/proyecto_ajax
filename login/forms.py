from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group

# class CustomLoginForm(AuthenticationForm):
#     # Puedes personalizar el formulario aquí si es necesario

#     # Agregar campos adicionales o personalizar los campos existentes
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
#     )
    
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
#     )