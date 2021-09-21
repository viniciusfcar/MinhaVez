from django.urls import path
from .views import cadastroAgendamentoAutorizacao
from .views import deleteAgendamento
from .views import detalhesAgendamento
from .views import adicionaUsuarioAgendamento
from .views import excluiUsuarioAgendamento
from .views import listaAgendamento
from .views import cadastroAgendamentoConsulta
from .views import detalhesAgendamentoUsuario
from .views import relatorioAgendamento
from .views import cadastroAgendamentoExame
from .views import relatorioListaAgendamento

urlpatterns = [
    path('lista_agendamento/', listaAgendamento, name='listaAgendamento'),
    path('cadastro_agendamento_autorizacao/<int:id>/', cadastroAgendamentoAutorizacao, name='cadastroAgendamentoAutorizacao'),
    path('delete_agendamento/<int:id>/', deleteAgendamento, name='deleteAgendamento'),
    path('detalhes_agendamento/<int:id>/', detalhesAgendamento, name='detalhesAgendamento'),
    path('adiciona_usuario_agendamento/<int:id>/', adicionaUsuarioAgendamento, name='adicionaUsuarioAgendamento'),
    path('exclui_usuario_agendamento/<int:idUser>/<int:id>/', excluiUsuarioAgendamento, name='excluiUsuarioAgendamento'),
    path('cadastro_agendamento_consulta/<int:id>/', cadastroAgendamentoConsulta, name='cadastroAgendamentoConsulta'),
    path('detalhes_agendamento_usuario/<int:id>/', detalhesAgendamentoUsuario, name='detalhesAgendamentoUsuario'),
    path('relatorio_agendamento/', relatorioAgendamento, name='relatorioAgendamento'),
    path('cadastro_agendamento_exame/<int:id>/', cadastroAgendamentoExame, name='cadastroAgendamentoExame'),
    path('relatorio_lista_agendamento/', relatorioListaAgendamento, name='relatorioListaAgendamento'),
]
