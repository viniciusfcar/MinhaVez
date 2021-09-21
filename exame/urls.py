from django.urls import path
from .views import cadastroExame
from .views import listaExame
from .views import alterarExame
from .views import deleteExame
from .views import detalhesExame
from .views import iniciarExame
from .views import encerrarExame
from .views import listaExameUsuario
from .views import detalhesExameUsuario
from .views import relatorioExame
from .views import relatorioListaExame
from .views import iniciarExame
from .views import listaExamesAguardando

urlpatterns = [
    path('cadastro_exame/', cadastroExame, name='cadastroExame'),
    path('lista_exame/', listaExame, name='listaExame'),
    path('alterar_exame/<int:id>/', alterarExame, name='alterarExame'),
    path('delete_exame/<int:id>/', deleteExame, name='deleteExame'),
    path('detalhes_exame/<int:id>/', detalhesExame, name='detalhesExame'),
    path('iniciar_exame/<int:id>/', iniciarExame, name='iniciarExame'),
    path('encerrar_exame/<int:id>/', encerrarExame, name='encerrarExame'),
    path('lista_exame_usuario/', listaExameUsuario, name='listaExameUsuario'),
    path('detalhes_exame_usuario/<int:id>/', detalhesExameUsuario, name='detalhesExameUsuario'),
    path('relatorio_exame/', relatorioExame, name='relatorioExame'),
    path('relatorio_lista_exame/', relatorioListaExame, name='relatorioListaExame'),
    path('iniciar_exame/<int:id/', iniciarExame, name='iniciarExame'),
    path('lista_exames_aguardando/', listaExamesAguardando, name='listaExamesAguardando'),
]