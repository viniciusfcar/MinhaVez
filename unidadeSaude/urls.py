from django.urls import path
from .views import alterarUnidadeSaude
from .views import cadastroUnidadeSaude
from .views import detalhesUnidadeSaude
from .views import listaUnidadeSaudeUsuario
from .views import listaUnidadeSaudeAdm
from .views import perfilUnidadeSaude
from .views import alterarPerfilUnidade
from .views import listaConsultasUnidade
from .views import listaAutorizacoesUnidade
from .views import listaExamesUnidade
from .views import listaEspecialistasUnidade
from .views import listaResponsaveisUnidade
from .views import listaUsuariosUnidade
from .views import novoUserUnidade
from .views import detalhesUnidadeAdm

urlpatterns = [
    path('alterar_unidade_saude/<int:id>/', alterarUnidadeSaude, name='alterarUnidadeSaude'),
    path('cadastro_unidade_saude/', cadastroUnidadeSaude, name='cadastroUnidadeSaude'),
    path('detalhes_unidade_saude/<int:id>/', detalhesUnidadeSaude, name='detalhesUnidadeSaude'),
    path('lista_unidade_saude_usuario/', listaUnidadeSaudeUsuario, name='listaUnidadeSaudeUsuario'),
    path('lista_unidade_saude_adm/', listaUnidadeSaudeAdm, name='listaUnidadeSaudeAdm'),
    path('perfil_unidade_saude/', perfilUnidadeSaude, name='perfilUnidadeSaude'),
    path('alterar_perfil_unidade/<int:id>/', alterarPerfilUnidade, name='alterarPerfilUnidade'),
    path('lista_consultas_unidade/<int:id>/', listaConsultasUnidade, name='listaConsultasUnidade'),
    path('lista_autorizacoes_unidade/<int:id>/', listaAutorizacoesUnidade, name='listaAutorizacoesUnidade'),
    path('lista_exames_unidade/<int:id>/', listaExamesUnidade, name='listaExamesUnidade'),
    path('lista_especialistas_unidade/<int:id>/', listaEspecialistasUnidade, name='listaEspecialistasUnidade'),
    path('lista_responsaveis_unidade/<int:id>/', listaResponsaveisUnidade, name='listaResponsaveisUnidade'),
    path('lista_usuarios_unidade/', listaUsuariosUnidade, name='listaUsuariosUnidade'),
    path('novo_user_unidade/', novoUserUnidade, name='novoUserUnidade'),
    path('detalhes_unidade_adm/<int:id>/', detalhesUnidadeAdm, name='detalhesUnidadeAdm'),
]
