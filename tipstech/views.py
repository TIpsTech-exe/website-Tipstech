from django.shortcuts import render
import requests
import feedparser
from django.http import HttpResponse, JsonResponse
from .models import Comentarios
from .forms import adicionarComentario
from django.utils.dateformat import format

def home(request):
    return render(request, 'home.html')

def servicos(request):
    return render(request, 'servicos.html')

def noticias(request):
    feed = feedparser.parse(
        'https://feeds.feedburner.com/canaltechbr'
    )

    palavras_chave = [
        'hardware',
        'software',
        'segurança',
        'cybersecurity',
        'android',
        'python',
        'javascript',
        'java',
        'php',
        'django',
        'vue',
        'react',

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
        {'noticias': noticias[:25]}
    )

def projetos(request):
    return render(request, 'projetos.html') 

def ok(request):
    if request.method == "POST":
        form = adicionarComentario(request.POST)

        if form.is_valid():

            nome = form.cleaned_data['nome']

            # 🔥 conta comentários desse nome
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

def listar_comentarios(request):
    comentarios = []

    for c in Comentarios.objects.all().order_by('-id'):
        comentarios.append({
            'id': c.id,
            'nome': c.nome,
            'comentado': c.comentado,
            'qtd_likes': c.qtd_likes,
            'data_da_postagem': format(c.data_da_postagem, 'd/m/Y H:i')
        })

    return JsonResponse(comentarios, safe=False)

from django.http import JsonResponse
from .models import Comentarios

def curtir_comentario(request, id):
    comentario = Comentarios.objects.get(id=id)

    curtidos = request.session.get('comentarios_curtidos', [])

    if id in curtidos:
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