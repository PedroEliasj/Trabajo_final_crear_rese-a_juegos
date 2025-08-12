import os
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from apps.blog.models import Juegos
from apps.login.form import RegistroUsuarioForm
from apps.login.funcionesMod import RegistroUsuario
from .models import PerfilUsuario
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.

def signup(request):

    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                servicio = RegistroUsuario(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    is_superuser=form.cleaned_data.get('is_superuser', False),
                    apellido=form.cleaned_data.get('apellido'),
                    fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento'),
                    imagen=form.cleaned_data.get('imagen')
                )
                servicio.registrar()
                return render(request, "login/signup.html", {
                    "form": RegistroUsuarioForm(),  # reset form
                    "mensaje": "Usuario registrado correctamente."
                })
            except Exception as e:
                return render(request, "login/signup.html", {
                    "form": form,
                    "mensaje": f"Error al registrar usuario: {e}"
                })
        else:
            return render(request, "login/signup.html", {
                "form": form
            })

    return render(request, "login/signup.html", {
        "form": RegistroUsuarioForm()
    })

def signin(request):

    if request.method == 'GET':
        return render(request, 'login/signin.html', {
            'form': AuthenticationForm()
        })
    else:
        email = request.POST.get('email', 'email No existe').strip()
        password = request.POST.get('password', 'password no existe')
        # email = request.POST['email']
        # password = request.POST['password']

        user_obj = User.objects.filter(email=email).first()

        if user_obj is None:
            return render(request, 'login/signin.html', {
                'form': AuthenticationForm(),
                'error': 'Email no encontrado'
            })

        user = authenticate(request, username=user_obj.username, password=password)

        if user is None:
            return render(request, 'login/signin.html', {
                'form': AuthenticationForm(),
                'error': 'Contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('apps.blog:home')

@login_required
def signout(request):
    logout(request)
    return redirect('apps.blog:home')

# @login_required
# def ver_perfil(request):
#     perfil = PerfilUsuario.objects.get(user=request.user)
#     return render(request, 'login/perfil.html', {'perfil': perfil})

# @login_required
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
        'perfil': perfil,
        'perfil_logueado' : request.user.perfilusuario
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

@login_required
def perfil_view(request):
    perfil = get_object_or_404(PerfilUsuario, user=request.user)
    juegos = Juegos.objects.filter(autor=request.user)
    return render(request, 'login/perfil.html', {
        'perfil': perfil,
        'juegos': juegos
    })
