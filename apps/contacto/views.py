from django.shortcuts import get_object_or_404, render, redirect

from apps.login.models import PerfilUsuario
from .forms import ContactoForm
from .models import Contacto
from django.contrib import messages

def contacto_view(request):
    perfil = None
    if request.user.is_authenticated:
        perfil = get_object_or_404(PerfilUsuario, user=request.user)

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            Contacto.objects.create(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                mensaje=form.cleaned_data['mensaje']
            )
            messages.success(request, '¡Gracias por tu mensaje!')
            return redirect('contacto')
    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {
        'form': form,
        'perfil': perfil
    })
