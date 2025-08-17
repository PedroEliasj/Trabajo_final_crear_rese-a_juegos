from django import forms
from .models import Juegos, Categoria

class PostForm(forms.ModelForm):
    class Meta:
        model = Juegos
        fields = ['titulo', 'categoria', 'descripcion', 'imagen']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'input-field',
                'id': 'titulo',
                'placeholder': 'Título',
                'required': 'required',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'descripcion',
                'id': 'descripcion',
                'rows': 5,
                'placeholder': 'Escribe la reseña...',
                'required': 'required',
            }),
            'categoria': forms.Select(attrs={
                'class': 'select-field',
                'id': 'categoria',
                # 'required': 'required',
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'file-input',
                'id': 'post-pic-input',
                'accept': 'image/*',
                'style': 'display:none;',
            }),
        }