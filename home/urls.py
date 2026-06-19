from django.contrib import admin
from django.urls import path
from tipstech import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('servicos/', views.servicos, name='servicos'),
    path('noticias/', views.noticias, name='noticias'),
    path('projetos/', views.projetos, name='projetos'),

    path('comentario/', views.ok, name='adicionarComentario'),
    path('listar-comentarios/', views.listar_comentarios),

    path('curtir/<int:id>/', views.curtir_comentario),
]