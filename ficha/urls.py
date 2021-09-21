from django.urls import path
from .views import cadastroFichaConsulta
from .views import cadastroFichaAutorizacao
from .views import deleteFicha
from .views import detalhesFicha
from .views import printPDF
from .views import cadastroFichaExame
from .views import cadastroFichaAgendamento

urlpatterns = [
    path('cadastro_ficha_consulta/<int:id>/', cadastroFichaConsulta, name='cadastroFichaConsulta'),
    path('cadastro_ficha_autorizacao/<int:id>/', cadastroFichaAutorizacao, name='cadastroFichaAutorizacao'),
    path('delete_ficha/<int:id>/', deleteFicha, name='deleteFicha'),
    path('detalhes_ficha/<int:id>/', detalhesFicha, name='detalhesFicha'),
    path('printPDF/', printPDF, name='printPDF'),
    path('cadastro_ficha_exame/<int:id>/', cadastroFichaExame, name='cadastroFichaExame'),
    path('cadastro_ficha_agendamento/<int:id>/', cadastroFichaAgendamento, name='cadastroFichaAgendamento'),
]
