from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 5:
            raise ValidationError("La contraseña debe tener al menos 5 caracteres.")
        return password1
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        dominios_permitidos = ['@ferromax.cl', '@gmail.com', '@hotmail.com']
        if not any(email.endswith(dominio) for dominio in dominios_permitidos):
            raise forms.ValidationError("Solo se permiten correos de los siguientes dominios: ferromax.cl, gmail.com, hotmail.com")
        return email