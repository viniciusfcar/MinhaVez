from django.urls import path
from .views import listaProfissao
from .views import cadastroProfissao
from .views import alterarProfissao
from .views import deleteProfissao

urlpatterns = [
    path('lista_profissoes/', listaProfissao, name='listaProfissao'),
    path('cadastro_profissao/', cadastroProfissao, name='cadastroProfissao'),
    path('alterar_profissao/<int:id>/', alterarProfissao, name='alterarProfissao'),
    path('delete_profissao/<int:id>/', deleteProfissao, name='deleteProfissao'),
]
