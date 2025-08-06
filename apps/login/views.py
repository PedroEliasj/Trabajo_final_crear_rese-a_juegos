import os
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from apps.login.funcionesMod import RegistroUsuario
from .models import PerfilUsuario
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_superuser = request.POST.get("is_superuser") == "on"
        apellido = request.POST.get("apellido")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        imagen = request.FILES.get("imagen")

        try:
            servicio = RegistroUsuario(
                username=username,
                email=email,
                password=password,
                is_superuser=is_superuser,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                imagen=imagen
            )
            servicio.registrar()
            mensaje = "Usuario registrado correctamente."
        except Exception as e:
            mensaje = f"Error al registrar usuario: {e}"

        return render(request, "login/signup.html", {"mensaje": mensaje})

    return render(request, "login/signup.html")

def signin(request):

    if request.method == 'GET':
        return render(request, 'login/signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], 
                            password=request.POST['password'])
        if user is None: 
            return render(request, 'login/signin.html', {
                'form' : AuthenticationForm,
                'error' : 'Contraseña no valida'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def ver_perfil(request):
    perfil = PerfilUsuario.objects.get(user=request.user)
    return render(request, 'login/perfil.html', {'perfil': perfil})

@login_required
def usuarios_list(request):
    usuarios = User.objects.all()
    return render(request, 'login/usuarios_list.html', {'usuarios': usuarios})

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    perfil = get_object_or_404(PerfilUsuario, user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        perfil.apellido = request.POST.get('apellido')
        perfil.fecha_nacimiento = request.POST.get('fecha_nacimiento')

        if 'imagen' in request.FILES:
            perfil.imagen = request.FILES['imagen']

        user.save()
        perfil.save()
        return redirect('usuarios_list')  # Redirige después de editar

    return render(request, 'login/editar_usuario.html', {
        'user': user,
        'perfil': perfil
    })

@login_required
def eliminar_usuario(request, user_id):

    user = get_object_or_404(User, id=user_id)

    try:
        perfil = PerfilUsuario.objects.get(user=user)

        # Si tiene imagen, la borra del sistema de archivos
        if perfil.imagen:
            imagen_path = perfil.imagen.path
            if os.path.isfile(imagen_path):
                os.remove(imagen_path)

        perfil.delete()

    except PerfilUsuario.DoesNotExist:
        pass

    user.delete()
    return redirect('login/usuarios_list')

# Viste prueba recuperacion usuario

def enviar_correo_prueba(request):
    try:
        send_mail(
            subject='Correo de prueba desde Django',
            message='¡Este es un correo de prueba! Si lo recibiste, tu configuración SMTP está funcionando.',
            from_email=None,  # Usa DEFAULT_FROM_EMAIL del settings
            recipient_list=['tucorreo@gmail.com'],  # Reemplazalo por el correo que querés probar
            fail_silently=False,
        )
        return HttpResponse("Correo enviado correctamente.")
    except Exception as e:
        return HttpResponse(f"Error al enviar correo: {e}")