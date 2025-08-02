from django.urls import path
from .views import contacto_view

urlpatterns = [
    path('', contacto_view, name='contacto'),  # <-- este 'contacto' debe coincidir con {% url 'contacto' %}
]
