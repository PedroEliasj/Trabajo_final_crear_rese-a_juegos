from django.shortcuts import render, redirect
from .forms import ContactoForm
from .models import Contacto
from django.contrib import messages

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            Contacto.objects.create(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                mensaje=form.cleaned_data['mensaje']
            )
            messages.success(request, '¡Gracias por tu mensaje!')
            return redirect('contacto')  # Reemplazá con el nombre de tu url
    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {'form': form})
