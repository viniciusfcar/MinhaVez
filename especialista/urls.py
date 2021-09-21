from django.urls import path
from .views import listaEspecialista
from .views import cadastroEspecialista
from .views import alterarEspecialista
from .views import deleteEspecialista
from .views import listaEspecilistaUsuario
from .views import detalhesEspecialistaUsuario
from .views import relatorioEspecialista
from .views import vinculaEspecialistaUnidade

urlpatterns = [
    path('lista_especialista/', listaEspecialista, name='listaEspecialista'),
    path('cadastro_especialista/', cadastroEspecialista, name='cadastroEspecialista'),
    path('alterar_especialista/<int:id>/', alterarEspecialista, name='alterarEspecialista'),
    path('delete_especialista/<int:id>/', deleteEspecialista, name='deleteEspecialista'),
    path('lista_especialista_usuario/', listaEspecilistaUsuario, name='listaEspecialistaUsuario'),
    path('detalhes_especialista_usuario/<int:id>/', detalhesEspecialistaUsuario, name='detalhesEspecialistaUsuario'),
    path('relatorio_especialista/', relatorioEspecialista, name='relatorioEspecialista'),
    path('vincula_especialista_unidade/', vinculaEspecialistaUnidade, name='vinculaEspecialistaUnidade'),
]
