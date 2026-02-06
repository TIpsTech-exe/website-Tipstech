from django import forms
from .models import Dicas

class adicionarDica(forms.ModelForm):
    class Meta:
        model = Dicas
        fields = ['titulo', 'descricao']   
    