from django.urls import path
from .views import configuracoes_unidade
from .views import alterarUsernameUserUnidade
from .views import alterarSenhaUserUnidade
from .views import configuracoesUsuario
from .views import alterarUsernameUsuario
from .views import alterarEmailUsuario
from .views import alterarEmailUserUnidade

urlpatterns = [
    path('configuracoes_unidade/', configuracoes_unidade, name='configuracoes_unidade'),
    path('alterar_username_user_unidade/', alterarUsernameUserUnidade, name='alterarUsernameUserUnidade'),
    path('alterar_senha_user_unidade/', alterarSenhaUserUnidade, name='alterarSenhaUserUnidade'),
    path('configuracoes_usuario/', configuracoesUsuario, name="configuracoesUsuario"),
    path('alterar_username_usuario/', alterarUsernameUsuario, name='alterarUsernameUsuario'),
    path('alterar_email_usuario/', alterarEmailUsuario, name='alterarEmailUsuario'),
    path('alterar_email_user_unidade/', alterarEmailUserUnidade, name='alterarEmailUserUnidade'),
]