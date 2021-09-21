from django.urls import path
from .views import listaConsulta
from .views import cadastroConsulta
from .views import alterarConsulta
from .views import deleteConsulta
from .views import detalhesConsulta
#from .views import adicionaUsuarioConsulta
#from .views import excluiUsuarioConsulta
from .views import listaConsultaUsuario
from .views import detalhesConsultaUsuario
from .views import iniciarConsulta
from .views import encerrarConsulta
from .views import relatorioConsulta
from .views import relatorioListaConsulta
from .views import listaConsultasAguardando

urlpatterns = [
    path('lista_consulta/', listaConsulta, name='listaConsulta'),
    path('cadastro_consulta/', cadastroConsulta, name='cadastroConsulta'),
    path('alterar_consulta/<int:id>/', alterarConsulta, name='alterarConsulta'),
    path('delete_consulta/<int:id>/', deleteConsulta, name='deleteConsulta'),
    path('detalhes_consulta/<int:id>/', detalhesConsulta, name='detalhesConsulta'),
    #path('adiciona_usuario_consulta/<int:id>/', adicionaUsuarioConsulta, name='adicionaUsuarioConsulta'),
    #path('exclui_usuario_consulta/<slug:cpf>/<int:id>/', excluiUsuarioConsulta, name='excluiUsuarioConsulta'),
    path('lista_consulta_usuario/', listaConsultaUsuario, name='listaConsultaUsuario'),
    path('detalhes_consulta_usuario/<int:id>/', detalhesConsultaUsuario, name='detalhesConsultaUsuario'),
    path('iniciar_consulta/<int:id>/', iniciarConsulta, name='iniciarConsulta'),
    path('encerrar_consulta/<int:id>/', encerrarConsulta, name='encerrarConsulta'),
    path('relatorio_consulta/', relatorioConsulta, name='relatorioConsulta'),
    path('relatorio_lista_consulta/', relatorioListaConsulta, name='relatorioListaConsulta'),
    path('lista_consultas_aguardando/', listaConsultasAguardando, name='listaConsultasAguardando'),
]
