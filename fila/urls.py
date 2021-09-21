from django.urls import path
from .views import listaFila
from .views import cadastroFilaConsulta
from .views import cadastroFilaAutorizacao
from .views import deleteFila
from .views import detalhesFila
from .views import naoCompareceu
from .views import relatorioFila
from .views import cadastroFilaExame
from .views import adicionarUsuarioFila

urlpatterns = [
    path('lista_fila/', listaFila, name='listaFila'),
    path('cadastro_fila_consulta/<int:id>/', cadastroFilaConsulta, name='cadastroFilaConsulta'),
    path('cadastro_fila_autorizacao/<int:id>/', cadastroFilaAutorizacao, name='cadastroFilaAutorizacao'),
    path('delete_fila/<int:id_fila>/<int:id_fila_pref>/', deleteFila, name='deleteFila'),
    path('detalhes_fila/<int:id>/', detalhesFila, name='detalhesFila'),
    path('nao_compareceu/<int:id>/', naoCompareceu, name='naoCompareceu'),
    path('relatorio_fila/', relatorioFila, name='relatorioFila'),
    path('cadastro_fila_exame/<int:id>/', cadastroFilaExame, name='cadastroFilaExame'),
    path('adicionar_usuario_fila/<int:id>', adicionarUsuarioFila, name='adicionarUsuarioFila'),
]
