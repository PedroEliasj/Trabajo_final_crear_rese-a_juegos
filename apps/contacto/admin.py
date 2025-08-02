from django.contrib import admin
from .models import Contacto

class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'mensaje', 'fecha')  # Mostrá estos campos en la lista
    search_fields = ('nombre', 'email')  # Activá búsqueda por nombre y email

admin.site.register(Contacto, ContactoAdmin)
