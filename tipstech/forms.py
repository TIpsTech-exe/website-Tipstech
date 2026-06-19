from django import forms
from .models import Comentarios

class adicionarComentario(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['nome', 'comentado']   
    