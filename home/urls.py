
from django.contrib import admin
from django.urls import path
from tipstech import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('teste', views.teste, name='teste'),
    path('dicas', views.dicas, name='dicas'),
    path('inserir', views.inserir, name='inserir'),
    path('ok', views.ok, name='ok'),
]
