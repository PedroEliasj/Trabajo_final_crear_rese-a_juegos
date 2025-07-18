from django.contrib import admin

from .models import Categoria, Juegos
# Register your models here.

class LibroAdmin(admin.ModelAdmin):
    # campos a mostrar a la hora de agregar un nuevo registro
    fields = ('titulo', 'autor' )
    # definimos campos a visualizar cuando ingresemos al modelo administrador
    list_display = ('titulo',)
    # definimos campo por el cual realizaremos busqueda en nuestro administrador
    search_fields = ('titulo',)
    # cuadro de filtrado por el campo seleccionado
    list_filter = ('fecha_agregado')

admin.site.register(Categoria)
admin.site.register(Juegos)
