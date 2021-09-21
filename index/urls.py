from django.urls import path
from .views import index
from .views import contatos
from .views import quemSomos 


urlpatterns = [
    path('', index, name='index'),
    path('contatos/', contatos, name='contatos'),
    path('quem_somos/', quemSomos, name='quemSomos'),
]