from django.shortcuts import render
from django.http import HttpResponse
from .models import Dicas
from .forms import adicionarDica    

def home(request):
    return HttpResponse("Bem-vindo ao Tipstech!")

def teste(request):
    return render(request, 'teste.html')

def dicas(request):
    dicasTech = Dicas.objects.all()
    saida = '<html><table border=1>'
    for dica in dicasTech:
        saida += f'<tr><td>{dica.titulo}</td><td>{dica.descricao}</td></tr>'    
    saida += '</table></html>'
    return HttpResponse(saida)  

def inserir(request):
    form = adicionarDica()
    return render(request, 'inserir.html', {'form': form})   

def ok(request):   
    form = adicionarDica(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("Dica inserida com sucesso!")
    else:
        return HttpResponse("Erro ao inserir a dica. Verifique os dados e tente novamente.")