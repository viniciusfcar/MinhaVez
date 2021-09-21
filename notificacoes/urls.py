from django.urls import path
from .views import listaNotificacoes
from .views import lerNotificacao
from .views import deleteNotificacao

urlpatterns = [
   path('lista_notificacoes/', listaNotificacoes, name='listaNotificacoes'),
   path('ler_notificacao/<int:id>/', lerNotificacao, name='lerNotificacao'),
   path('delete_notificacao/<int:id>/', deleteNotificacao, name='deleteNotificacao'),
]
