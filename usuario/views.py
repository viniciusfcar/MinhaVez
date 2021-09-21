from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import FormUsuario
from .forms import FormUser
from django.contrib.auth.models import User
from ficha.models import Ficha
from fila.models import Fila
from consulta.models import Consulta
from autorizacao.models import Autorizacao
from exame.models import Exame
from agendamento.models import Agendamento
from rolepermissions.roles import assign_role
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UsuarioSerializer, UserSerializer
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework import serializers as serial
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.filters import SearchFilter
from django.core.mail import send_mail
from accounts import views as views_accounts
from drf_extra_fields.fields import Base64ImageField
import base64
import re
import struct
import binascii
from django.core.files.base import ContentFile
from .serializers import ImageSerializer

class ImagemUpload(APIView):
    
    def post(self, request, *args, **kwargs):
        serializers = ImageSerializer(data=request)
        if serializers.is_valid():
            return serializers.data

class GetUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer  
    filter_backends = (SearchFilter,)
    search_fields = ['=cpf', '=sus']

    def get_queryset(self):
        queryset = Usuario.objects.all()
        return queryset

    @action(methods=['get'], detail=True)
    def minhasFichas(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        fichas = Ficha.objects.filter(usuario=usuario, excluida=False).order_by('status')
        tmpJson = serializers.serialize("json", fichas)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))
    

    @action(methods=['post'], detail=False)
    @permission_classes([])
    def verificaUser(self, request):
        token = request.POST.get('token')
        user = User.objects.filter(auth_token=token)
        usuario = Usuario.objects.filter(user=user[0])
        tmpJson = serializers.serialize("json", usuario)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

    @action(methods=['post'], detail=False)
    def set_notificacao(self, request):
        token = request.POST.get('token')
        token = token.replace('"', '')
        user = User.objects.filter(auth_token=token)
        usuario = Usuario.objects.filter(user=user[0])
        if usuario:
            if request.method == 'POST':
                usuario[0].notificacao = request.POST.get('notificacao')
                usuario[0].save()
                return HttpResponse(status=status.HTTP_200_OK)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False)
    def alterar_senha(self, request):

        try:
            views_accounts.password_reset_request(request)
            return HttpResponse(status=status.HTTP_200_OK)
        except expression as identifier:
            pass

    @action(methods=['post'], detail=False)
    def cadastro_user(self, request):
        new_user = User.objects.filter(username=request.POST.get('username'))
        user_cpf = Usuario.objects.filter(cpf=request.POST.get('cpf'))
        user_sus = Usuario.objects.filter(sus=request.POST.get('sus'))

        if request.method == 'POST':
            try:
                validate_email(request.POST.get('email'))
                valid_email = True
            except ValidationError:
                valid_email = False

            if valid_email:
                if not new_user and not user_cpf and not user_sus:
                    
                    password = request.POST.get('password')

                    usuario = Usuario(cpf=request.POST.get('cpf'), rg=request.POST.get('rg'), sus=request.POST.get('sus'),
                                    logradouro=request.POST.get('logradouro'), cep=request.POST.get('cep'), sexo=request.POST.get('sexo'),
                                    numero=request.POST.get('numero'), complemento=request.POST.get('complemento'), telefone=request.POST.get('telefone'),
                                    bairro=request.POST.get('bairro'), cidade=request.POST.get('cidade'), estado=request.POST.get('estado'))

                    user = User(username=request.POST.get('username'), first_name=request.POST.get('first_name'),
                                last_name=request.POST.get('last_name'), email=request.POST.get('email'))
                    
                    user.set_password(password)
                    user.save()
                    usuario.user = user
                    usuario.save()
                    Token.objects.create(user=user)
                    assign_role(user, 'usuario')
                    
                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_409_CONFLICT)
            else:
                return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def editar_perfil(self, request):
        token = request.POST.get('token')
        token = token.replace('"', '')
        user = User.objects.filter(auth_token=token)
        usuario = Usuario.objects.filter(user=user[0])

        if user and usuario:
            user_cpf = Usuario.objects.filter(cpf=request.POST.get('cpf'))
            user_sus = Usuario.objects.filter(sus=request.POST.get('sus'))

            if user_cpf[0] == None or user_cpf[0].user == user[0]:
                if user_sus[0] == None or user_sus[0].user == user[0]:
                    user[0].first_name = request.POST.get('first_name')
                    user[0].last_name = request.POST.get('last_name')
                    usuario[0].cpf = request.POST.get('cpf')
                    usuario[0].rg = request.POST.get('rg')
                    usuario[0].sus = request.POST.get('sus')
                    usuario[0].cep = request.POST.get('cep')
                    usuario[0].logradouro = request.POST.get('logradouro')
                    usuario[0].numero = request.POST.get('numero')
                    usuario[0].complemento = request.POST.get('complemento')
                    usuario[0].bairro = request.POST.get('bairro')
                    usuario[0].cidade = request.POST.get('cidade')
                    usuario[0].estado = request.POST.get('estado')
                    usuario[0].sexo = request.POST.get('sexo')
                    usuario[0].telefone = request.POST.get('telefone')
                    user[0].save()
                    usuario[0].save()
                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_409_CONFLICT)
            else:
                return HttpResponse(status=status.HTTP_409_CONFLICT)     
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False)
    def editar_foto_perfil(self, request):
        token = request.POST.get('token')
        token = token.replace('"', '')
        user = User.objects.filter(auth_token=token)
        usuario = Usuario.objects.filter(user=user[0])

        if usuario:
            try:
                #PRECISO TRANSFORMAR A STRING EM BYTE
                image_data = request.POST.get('avatar')
                usuario[0].imagem = image_data
                usuario[0].save
                
                return HttpResponse(status=status.HTTP_200_OK)
            except Exception as identifier:
                print(identifier)
                return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)
            
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['post'], detail=False)
    def editar_email(self, request):
        token = request.POST.get('token')
        token = token.replace('"', '')
        email = request.POST.get('email')
        new_email = request.POST.get('new_email')
        user = User.objects.filter(auth_token=token)

        if user:
            try:
                validate_email(request.POST.get('new_email'))
                valid_email = True
            except ValidationError:
                valid_email = False
            
            if valid_email:
                if user[0].email == email:
                    if email != new_email:
                        
                        user[0].email = new_email
                        user[0].save()

                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return HttpResponse(status=HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

    @action(methods=['post'], detail=False)
    def editar_username(self, request):
        token = request.POST.get('token')
        token = token.replace('"', '')
        username = request.POST.get('username')
        new_username = request.POST.get('new_username')

        user = User.objects.filter(auth_token=token)
        user_username = User.objects.filter(username=new_username)
        
        if user:
            if user[0].username == username:
                if not user_username:
                    if username != new_username:
                        
                        user[0].username = new_username
                        user[0].save()

                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return HttpResponse(status=HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

    @action(methods=['get'], detail=True)
    def total_notificacao_app(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        total_not = usuario.notificacoes.filter(status=False).count()
        tmpObj = json.loads(total_not.__str__())
        return HttpResponse(json.dumps(tmpObj))

    @action(methods=['get'], detail=True)
    def lista_notificacoes(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        notificacoes = usuario.notificacoes.order_by('status')
        tmpJson = serializers.serialize("json", notificacoes)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))
    
    @action(methods=['get'], detail=False)
    def total_notificacao(self, request):
        usuario = Usuario.objects.get(user=request.user)
        total_not = usuario.notificacoes.filter(status=False).count()
        tmpObj = json.loads(total_not.__str__())
        return HttpResponse(json.dumps(tmpObj))

class GetUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer  
    filter_backends = (SearchFilter,)
    search_fields = ['=username']

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

def cadastroUsuario(request):

    form = FormUsuario()
    context = {
        'form': form,
    }

    if request.method == 'POST':
        
        user = User.objects.filter(username=request.POST.get('username'))
        confirm_password = request.POST.get('confirmPassword')
        password = request.POST.get('password')
        print(user)
        if user:

            context = {
                'form': FormUsuario(),
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'nome': request.POST.get('firstname'),
                'sobrenome': request.POST.get('lastname'),
                'rua': request.POST.get('rua'),
                'numero': request.POST.get('numero'),
                'bairro': request.POST.get('bairro'),
                'cidade': request.POST.get('cidade'),
                'complemento': request.POST.get('completo'),
                'estado': request.POST.get('estado'),
                'cpf': request.POST.get('cpf'),
                'sus': request.POST.get('sus'),
                'sexo': request.POST.get('sexo'),
                'rg': request.POST.get('rg'),
                'msg': 'Já existe usuario com esse username, escolha outro'
            }

            return render(request, 'cadastro_usuario.html', {'context': context})
        
        elif confirm_password != password:

            context = {
                'form': form,
                'msg': 'Senhas não conferem.'
            }

            return render(request, 'cadastro_usuario.html', {'context': context})
        else:

            usuario = Usuario(cpf=request.POST.get('cpf'), rg=request.POST.get('rg'), sus=request.POST.get('sus'),
                            logradouro=request.POST.get('logradouro'), cep=request.POST.get('cep'), sexo=request.POST.get('sexo'),
                            numero=request.POST.get('numero'), complemento=request.POST.get('complemento'), telefone=request.POST.get('telefone'),
                            bairro=request.POST.get('bairro'), cidade=request.POST.get('cidade'), estado=request.POST.get('estado'), imagem=request.FILES['imagem'])

            user = User(username=request.POST.get('username'), first_name=request.POST.get('firstname'),
                        last_name=request.POST.get('lastname'), email=request.POST.get('email'))

            user.set_password(password)
            user.save()
            usuario.user = user
            usuario.save()
            Token.objects.create(user=user)
            assign_role(user, 'usuario')

            msg = "Cadastro realizado com sucesso, faça já o seu login."
            
            return render(request, 'index.html', {'msg_cadastro': msg})

    return render(request, 'cadastro_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaUsuario(request):
    usuarios = Usuario.objects.all()

    return render(request, 'lista_usuario.html', {'atendimentos': usuarios})


@login_required(login_url='/accounts/login')
def alterarPerfil(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        
        usuario = get_object_or_404(Usuario, pk=id)
        form = FormUsuario(request.POST or None, request.FILES or None, instance=usuario)

        context = {
            'form': form,
            'usuario': usuario
        }

        if request.method == 'POST':

            if form.is_valid():
                usuario.user.first_name = request.POST.get('firstname')
                usuario.user.last_name = request.POST.get('lastname')
                usuario.logradouro = request.POST.get('logradouro')
                usuario.bairro = request.POST.get('bairro')
                usuario.numero = request.POST.get('numero')
                usuario.cidade = request.POST.get('cidade')
                usuario.estado = request.POST.get('estado')
                usuario.rg = request.POST.get('rg')
                usuario.cpf = request.POST.get('cpf')
                usuario.sexo = request.POST.get('sexo')
                usuario.sus = request.POST.get('sus')

                form.save()
                usuario.user.save()
                usuario.save()
            return render(request, 'perfil_usuario.html', {'usuario': usuario})

        return render(request, 'alterar_perfil.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def deleteUsuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    form = FormUsuario(request.POST or None, request.FILES or None, instance=usuario)

    if request.method == 'POST':
        usuario.delete()
        return redirect('listaUsuario')

    return render(request, 'delete_usuario.html', {'nome': usuario.nome})


@login_required(login_url='/accounts/login')
def detalhesUsuario(request, id, id_sec):
    if has_permission(request.user, 'permissao_unidade'):
        usuario = get_object_or_404(Usuario, pk=id)
        agendamento = None
        fila = None
        
        try:
            agendamento = Agendamento.objects.get(id=id_sec)
        except:
            fila = Fila.objects.get(id=id_sec)

        if agendamento:

            context = {
                'usuario': usuario,
                'agendamento': agendamento,
            }

            return render(request, 'detalhes_usuario.html', {'context': context})
        
        elif fila:

            context = {
                'usuario': usuario,
                'fila': fila,
            }

            return render(request, 'detalhes_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def minhasFichas(request):
    if has_permission(request.user, 'permissao_usuario'):
        usuario = Usuario.objects.filter(user=request.user)
        fichas = Ficha.objects.filter(usuario=usuario[0], excluida=False).order_by('status')
        pesquisa = request.GET.get('pesquisa')

        if pesquisa:
            fichas = fichas.filter(numero__icontains=pesquisa).order_by('status') | fichas.filter(status__icontains=pesquisa).order_by('status')

            if fichas:
                context = {
                    'fichas': fichas,
                }

            else:
                fichas = Ficha.objects.filter(usuario=usuario[0]).order_by('status')
                context = {
                    'fichas': fichas,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }

        elif fichas:

            context = {
                'fichas': fichas,
            }

        else:
            context = {
                'msg_alert': 'Você não possue nenhuma ficha!'
            }

        return render(request, 'minhas_fichas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def meusAgendamentos(request):
    if has_permission(request.user, 'permissao_usuario'):
        usuario = Usuario.objects.filter(user=request.user)
        agendamentos = Agendamento.objects.filter(usuarios=usuario[0])
        nome = request.GET.get('nome')
        
        if nome:
            agendamentos = agendamentos.filter(nome__icontains=nome)

            if agendamentos:
                context = {
                    'agendamentos': agendamentos
                }
            else:
                agendamentos = Agendamento.objects.filter(usuarios=usuario[0])
                context = {
                    'agendamentos': agendamentos,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }

        elif agendamentos:
            context = {
                'agendamentos': agendamentos
            }

        else:
            context = {
                'msg_alert': 'Você não participa de nenhum agendamento!'
            }

        return render(request, 'meus_agendamentos.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def perfilUsuario(request):
    if has_permission(request.user, 'permissao_usuario'):
        usuario = Usuario.objects.filter(user=request.user)

        return render(request, 'perfil_usuario.html', {'usuario': usuario[0]})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

