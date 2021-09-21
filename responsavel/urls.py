from django.urls import path
from .views import listaResponsavel
from .views import cadastroResponsavel
from .views import alterarResponsavel
from .views import deleteResponsavel
from .views import relatorioResponsavel

urlpatterns = [
    path('lista_responsavel/', listaResponsavel, name='listaResponsavel'),
    path('cadastro_responsavel/', cadastroResponsavel, name='cadastroResponsavel'),
    path('alterar_responsavel/<int:id>/', alterarResponsavel, name='alterarResponsavel'),
    path('delete_responsavel/<int:id>/', deleteResponsavel, name='deleteResponsavel'),
    path('relatorio_responsavel/', relatorioResponsavel, name='relatorioResponsavel')
]
