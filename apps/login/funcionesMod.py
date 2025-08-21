from apps.login.models import PerfilUsuario
from django.contrib.auth.models import User
import re

class RegistroUsuario:
    def __init__(self, username, email, password, is_superuser=False, apellido=None, fecha_nacimiento=None, imagen=None):
        self.username = username
        self.email = email
        self.password = password
        self.is_superuser = is_superuser
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.imagen = imagen

    def validar_contrasena(self):
        if len(self.password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r"[A-Z]", self.password):
            return "La contraseña debe contener al menos una letra mayúscula."
        if not re.search(r"\d", self.password):
            return "La contraseña debe contener al menos un número."
        if not re.search(r"[!@#$%&*]", self.password):
            return "La contraseña debe contener al menos un carácter especial (!@#$%&*)."
        return None

    def crear_usuario(self):
        if self.is_superuser:
            user = User.objects.create_superuser(
                username=self.username,
                email=self.email,
                password=self.password
            )
        else:
            user = User.objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password
            )
            user.is_staff = False
        user.save()
        return user

    def registrar(self):
        error = self.validar_contrasena()
        if error:
            raise ValueError(error)

        user = self.crear_usuario()

        perfil = PerfilUsuario.objects.create(
            user=user,
            apellido=self.apellido,
            fecha_nacimiento=self.fecha_nacimiento,
            imagen=self.imagen
        )
        perfil.save()

        return user