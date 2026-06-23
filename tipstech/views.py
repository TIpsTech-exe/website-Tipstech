from django.shortcuts import render
import requests
import feedparser
from django.http import HttpResponse, JsonResponse
from .models import Comentarios
from .forms import adicionarComentario
from django.utils.dateformat import format
from django.http import JsonResponse
from .models import Comentarios
from django.utils import timezone
from zoneinfo import ZoneInfo

def home(request):
    return render(request, 'home.html')

def servicos(request):
    return render(request, 'servicos.html')

def noticias(request):
 # API do canal techbr
    feed = feedparser.parse(
        'https://feeds.feedburner.com/canaltechbr'
    )
# fitro por plavras chaves relacionadas à tecnologias
    palavras_chave = [
        'hardware',
        'software',
        'cybersecurity',
        'android',
        'python',
        'javascript',
        'java',
        'php',
        'django',
        'vue',
        'react',
        'Sistemas Operacionais',
        'Notebooks',
        'Robótica',
        'Internet das Coisas',
        'Desenvolvimento Mobile',
        'Big Data',
        'Machine Learning',
        'Redes de Computadores',
    ]

    noticias = []

    for item in feed.entries:
        texto = (
            item.title + ' ' +
            item.get('summary', '')
        ).lower()
        if any(palavra.lower() in texto for palavra in palavras_chave):
            noticias.append({
                'titulo': item.title,
                'link': item.link,
                'resumo': item.get('summary', ''),
                'data': item.get('published', '')
            })
    return render(
        request,
        'noticias.html',
        {'noticias': noticias[:25]} # limite máximo de notícia
    )

def projetos(request):
    return render(request, 'projetos.html') 
# recebe o comentário do cliente
def ok(request):
    if request.method == "POST":
        form = adicionarComentario(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            total = Comentarios.objects.filter(nome=nome).count()
            if total >= 3:
                return JsonResponse({
                    "success": False,
                    "message": "Você atingiu o limite de 3 comentários."
                })
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Comentário enviado com sucesso!"
            })
        return JsonResponse({
            "success": False,
            "errors": form.errors
        })
    return JsonResponse({"success": False})
# manda o a lista de comentários em json para a página
def listar_comentarios(request):
    comentarios = []
    for c in Comentarios.objects.all().order_by('-id'):
        data_brasil = timezone.localtime(
            c.data_da_postagem,
            ZoneInfo("America/Fortaleza")
        )
        comentarios.append({
            'id': c.id,
            'nome': c.nome,
            'comentado': c.comentado,
            'qtd_likes': c.qtd_likes,
            'data_da_postagem': data_brasil.strftime('%d/%m/%Y %H:%M')
        })
    return JsonResponse(comentarios, safe=False)
# altera a qtd de curtida de um comentário 
def curtir_comentario(request, id):
    comentario = Comentarios.objects.get(id=id)
    curtidos = request.session.get('comentarios_curtidos', [])

    if id in curtidos: #limita uma curtida por comentário
        return JsonResponse({
            'success': False,
            'message': 'Você já curtiu este comentário.' 
        })

    comentario.qtd_likes += 1
    comentario.save()

    curtidos.append(id)
    request.session['comentarios_curtidos'] = curtidos

    return JsonResponse({
        'success': True,
        'likes': comentario.qtd_likes
    })