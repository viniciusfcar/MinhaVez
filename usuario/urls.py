from django.urls import path
from .views import listaUsuario
from .views import cadastroUsuario
from .views import alterarPerfil
from .views import deleteUsuario
from .views import detalhesUsuario
from .views import minhasFichas
from .views import meusAgendamentos
from .views import perfilUsuario
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('lista_usuario/', listaUsuario, name='listaUsuario'),
    path('cadastro_usuario/', cadastroUsuario, name='cadastroUsuario'),
    path('alterar_perfil/<int:id>/', alterarPerfil, name='alterarPerfil'),
    path('delete_usuario/<int:id>/', deleteUsuario, name='deleteUsuario'),
    path('detalhes_usuario/<int:id>/<int:id_sec>/', detalhesUsuario, name='detalhesUsuario'),
    path('minhas_fichas/', minhasFichas, name='minhasFichas'),
    path('meus_agendamentos/', meusAgendamentos, name='meusAgendamentos'),
    path('perfil_usuario/', perfilUsuario, name='perfilUsuario'),
]
