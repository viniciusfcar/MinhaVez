from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from home import urls as home_urls
from exame import urls as exame_urls
from profissao import urls as prof_urls
from especialista import urls as especialista_urls
from responsavel import urls as resp_urls
from autorizacao import urls as autori_urls
from usuario import urls as user_urls
from consulta import urls as consult_urls
from agendamento import urls as agendamento_urls
from accounts import urls as accounts_urls
from unidadeSaude import urls as und_saude_urls
from configuracoes import urls as configuracoes_urls
from index import urls as index_urls
from ficha import urls as ficha_urls
from fila import urls as fila_urls
from notificacoes import urls as notificacoes_urls
from rest_framework import routers
from agendamento.views import GetAgendamentoViewSet
from autorizacao.views import GetAutorizacaoViewSet
from consulta.views import GetConsultaViewSet
from especialista.views import GetEspecialistaViewSet
from ficha.views import GetFichaViewSet
from fila.views import GetFilaViewSet
from responsavel.views import GetResponsavelViewSet
from unidadeSaude.views import GetUnidadeSaudeViewSet
from usuario.views import GetUsuarioViewSet, GetUserViewSet
from profissao.views import GetProfissaoViewSet
from especializacao.views import GetEspecializacaoViewSet
from notificacoes.views import GetNotificacaoViewSet
from exame.views import GetExameViewSet
router = routers.DefaultRouter()
router.register(r'agendamento', GetAgendamentoViewSet, basename='Agendamento')
router.register(r'autorizacao', GetAutorizacaoViewSet, basename='Autorizacao')
router.register(r'consulta', GetConsultaViewSet, basename='Consulta')
router.register(r'especialista', GetEspecialistaViewSet, basename='Especialista')
router.register(r'ficha', GetFichaViewSet, basename='Ficha')
router.register(r'fila', GetFilaViewSet, basename='Fila')
router.register(r'responsavel', GetResponsavelViewSet)
router.register(r'unidade_saude', GetUnidadeSaudeViewSet, basename='UnidadeSaude')
router.register(r'usuario', GetUsuarioViewSet, basename='Usuario')
router.register(r'user', GetUserViewSet, basename='User')
router.register(r'profissao', GetProfissaoViewSet, basename='Profissao')
router.register(r'especializacao', GetEspecializacaoViewSet, basename='Especializacao')
router.register(r'exame', GetExameViewSet, basename='Exame')
router.register(r'notificacao', GetNotificacaoViewSet, basename='Notificacao')
from django.views.generic import RedirectView
from django.conf.urls import url 
from rest_framework.authtoken.views import obtain_auth_token   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include(home_urls)),
    path('profissao/', include(prof_urls)),
    path('especialista/', include(especialista_urls)),
    path('responsavel/', include(resp_urls)),
    path('autorizacao/', include(autori_urls)),
    path('usuario/', include(user_urls)),
    path('consulta/', include(consult_urls)),
    path('agendamento/', include(agendamento_urls)),
    path('accounts/', include(accounts_urls)),
    path('unidade_saude/', include(und_saude_urls)),
    path('', include(index_urls)),
    path('ficha/', include(ficha_urls)),
    path('fila/', include(fila_urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    path('api-token-auth/', obtain_auth_token),
    path('exame/', include(exame_urls)),
    path('configuracoes/', include(configuracoes_urls)),
    path('notificacoes/', include(notificacoes_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
