from django import forms
from django.core.exceptions import ValidationError
import re

class RegistroUsuarioForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=150, required=True)
    email = forms.EmailField(label="Correo electrónico", required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)
    confirmar_password = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, required=True)
    is_superuser = forms.BooleanField(label="¿Es superusuario?", required=False)
    apellido = forms.CharField(label="Apellido", max_length=150, required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    imagen = forms.ImageField(label="Imagen de perfil", required=False)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Za-z]", password):
            raise ValidationError("La contraseña debe contener al menos una letra.")
        if not re.search(r"\d", password):
            raise ValidationError("La contraseña debe contener al menos un número.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")

        if password and confirmar and password != confirmar:
            self.add_error("confirmar_password", "Las contraseñas no coinciden.")