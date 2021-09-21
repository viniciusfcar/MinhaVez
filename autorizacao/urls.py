from django.urls import path
from .views import listaAutorizacao
from .views import cadastroAutorizacao
from .views import alterarAutorizacao
from .views import deleteAutorizacao
from .views import detalhesAutorizacao
from .views import listaAutorizacaoUsuario
from .views import iniciarAutorizacao
from .views import encerrarAutorizacao
from .views import relatorioAutorizacao
from .views import detalhesAutorizacaoUsuario
from .views import relatorioListaAutorizacao
from .views import listaAutorizacoesAguardando

urlpatterns = [
    path('lista_autorizacao/', listaAutorizacao, name='listaAutorizacao'),
    path('cadastro_autorizacao/', cadastroAutorizacao, name='cadastroAutorizacao'),
    path('alterar_autorizacao/<int:id>/', alterarAutorizacao, name='alterarAutorizacao'),
    path('delete_autorizacao/<int:id>/', deleteAutorizacao, name='deleteAutorizacao'),
    path('detalhes_autorizacao/<int:id>/', detalhesAutorizacao, name='detalhesAutorizacao'),
    path('lista_autorizacao_usuario/', listaAutorizacaoUsuario, name='listaAutorizacaoUsuario'),
    path('iniciar_autorizacao/<int:id>/', iniciarAutorizacao, name='iniciarAutorizacao'),
    path('encerrar_autorizacao/<int:id>/', encerrarAutorizacao, name='encerrarAutorizacao'),
    path('relatorio_autorizacao/', relatorioAutorizacao, name='relatorioAutorizacao'),
    path('detalhes_autorizacao_usuario/<int:id>/', detalhesAutorizacaoUsuario, name='detalhesAutorizacaoUsuario'),
    path('relatorio_lista_autorizacao/', relatorioListaAutorizacao, name='relatorioListaAutorizacao'),
    path('lista_autorizacoes_aguardando/', listaAutorizacoesAguardando, name='listaAutorizacoesAguardando'),
]
