from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from fila.models import Fila
from ficha.models import Ficha
from usuario.models import Usuario
from django.contrib.auth.models import User
from consulta.models import Consulta
from agendamento.models import Agendamento
from .forms import FormFicha
from autorizacao.models import Autorizacao
from unidadeSaude.models import UnidadeSaude
from exame.models import Exame
from rest_framework import viewsets
from .serializers import FichaSerializer
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from weasyprint import HTML
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework import status
from notificacoes import views as notificacoes

class GetFichaViewSet(viewsets.ModelViewSet):
    serializer_class = FichaSerializer

    def get_queryset(self):
        queryset = Ficha.objects.all().order_by('status')
        return queryset

    @action(methods=['get'], detail=True)
    def consulta_posicao_ficha(self, request, pk=None):
        ficha = get_object_or_404(Ficha, pk=pk)
        filas = Fila.objects.filter(fichas=ficha)
        posicao = 0

        if filas:
            if filas[0].fichas.all():
                for fic in filas[0].fichas.all():
                    if fic == ficha:  
                        return HttpResponse(json.dumps(posicao))
                    else:
                        posicao += 1
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def cadastro_ficha_consulta(self, request):
        consulta = get_object_or_404(Consulta, pk=request.POST.get('id_consulta'))
        token = request.POST.get('token')
        token = token.replace('"', '')

        if token:
            user = User.objects.filter(auth_token=token)
            usuario = Usuario.objects.filter(user=user[0])
            permitido = True
            agendado = False
            fila_normal = None
            fila_preferencial = None

            if request.method == 'POST':
                if consulta.create_fila:
                    
                    for fila in consulta.filas.all():
                        if fila.fila_preferencial:
                            fila_preferencial = fila
                        else:
                            fila_normal = fila

                    for ficha in fila_normal.fichas.all():
                        if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                            permitido = False

                    for ficha in fila_preferencial.fichas.all():
                        if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                            permitido = False

                    if consulta.agendamento and consulta.agendamento.usuarios:
                        for user in consulta.agendamento.usuarios.all():
                            if user == usuario[0]:
                                agendado = True

                    if permitido:

                        preferencial = None

                        if request.POST.get('preferencial') == '0':
                            preferencial = False
                        else:
                            preferencial = True              
                            
                        if preferencial:
                            if fila_preferencial.vagas > 0:
                                ficha = Ficha()
                                ficha.numero = 0
                                ficha.preferencial = preferencial
                                ficha.usuario = usuario[0]
                                ficha.status = "AGUARDANDO"
                                ficha.excluida = False
                                ficha.save()

                                fila_preferencial.fichas.add(ficha)

                                gerarNumerosFichas(request, fila_preferencial)
                                
                                if agendado == False:
                                    fila_preferencial.vagas -= 1
                                    fila_normal.vagas -= 1

                                fila_preferencial.save()
                                fila_normal.save()

                                fichas = []
                                fichas.append(ficha)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                tmpJson = serializers.serialize("json", fichas)
                                tmpObj = json.loads(tmpJson)  
                                return HttpResponse(json.dumps(tmpObj))
                            else:
                                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

                        else:
                            if fila_normal.vagas > 0:
                                ficha = Ficha()
                                ficha.numero = 0                                
                                ficha.preferencial = preferencial
                                ficha.usuario = usuario[0]
                                ficha.status = "AGUARDANDO"
                                ficha.excluida = False
                                ficha.save()

                                fila_normal.fichas.add(ficha)

                                gerarNumerosFichas(request, fila_normal)

                                if agendado == False:
                                    fila_normal.vagas -= 1
                                    fila_preferencial.vagas -= 1

                                fila_normal.save()
                                fila_preferencial.save()
                                
                                fichas = []
                                fichas.append(ficha)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                tmpJson = serializers.serialize("json", fichas)
                                tmpObj = json.loads(tmpJson)  
                                return HttpResponse(json.dumps(tmpObj))
                            else:
                                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
                else:
                    return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)
    
    @action(methods=['post'], detail=False)
    def cadastro_ficha_autorizacao(self, request):
        autorizacao = get_object_or_404(Autorizacao, pk=request.POST.get('id_autorizacao'))
        token = request.POST.get('token')
        token = token.replace('"', '')
        
        if token:
            user = User.objects.filter(auth_token=token)
            usuario = Usuario.objects.filter(user=user[0])
            permitido = True
            agendado = False
            fila_normal = None
            fila_preferencial = None
            
            if request.method == 'POST':
                if autorizacao.create_fila:
                    
                    for fila in autorizacao.filas.all():
                        if fila.fila_preferencial:
                            fila_preferencial = fila
                        else:
                            fila_normal = fila

                    for ficha in fila_normal.fichas.all():
                        if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                            permitido = False

                    for ficha in fila_preferencial.fichas.all():
                        if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                            permitido = False

                    if autorizacao.agendamento and autorizacao.agendamento.usuarios:
                        for user in autorizacao.agendamento.usuarios.all():
                            if user == usuario[0]:
                                agendado = True

                    if permitido:

                        preferencial = None
                        
                        if request.POST.get('preferencial') == '0':
                            preferencial = False
                        else:
                            preferencial = True                        

                        if preferencial:
                            if fila_preferencial.vagas > 0:
                                ficha = Ficha()
                                ficha.numero = 0                                
                                ficha.preferencial = preferencial
                                ficha.usuario = usuario[0]
                                ficha.status = "AGUARDANDO"
                                ficha.excluida = False
                                ficha.save()

                                fila_preferencial.fichas.add(ficha)

                                gerarNumerosFichas(request, fila_preferencial)
                                
                                if agendado == False:
                                    fila_preferencial.vagas -= 1
                                    fila_normal.vagas -= 1

                                fila_preferencial.save()
                                fila_normal.save()
                                fichas = []
                                fichas.append(ficha)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                tmpJson = serializers.serialize("json", fichas)
                                tmpObj = json.loads(tmpJson)  
                                return HttpResponse(json.dumps(tmpObj))
                            else:
                                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            if fila_normal.vagas > 0:
                                ficha = Ficha()
                                ficha.numero = 0                                
                                ficha.preferencial = preferencial
                                ficha.usuario = usuario[0]
                                ficha.status = "AGUARDANDO"
                                ficha.excluida = False
                                ficha.save()

                                fila_normal.fichas.add(ficha)

                                gerarNumerosFichas(request, fila_normal)

                                if agendado == False:
                                    fila_normal.vagas -= 1
                                    fila_preferencial.vagas -= 1

                                fila_normal.save()
                                fila_preferencial.save()
                                fichas = []
                                fichas.append(ficha)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                tmpJson = serializers.serialize("json", fichas)
                                tmpObj = json.loads(tmpJson)  
                                return HttpResponse(json.dumps(tmpObj))
                            else:
                                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
                else:
                    return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

    @action(methods=['post'], detail=False)
    def cadastro_ficha_exame(self, request):
        exame = get_object_or_404(Exame, pk=request.POST.get('id_exame'))
        token = request.POST.get('token')
        token = token.replace('"', '')

        if token:
            user = User.objects.filter(auth_token=token)
            usuario = Usuario.objects.filter(user=user[0])
            permitido = True
            agendado = False
            fila_normal = None
            fila_preferencial = None

            if request.method == 'POST':
                if exame.create_fila:
                    
                    for fila in exame.filas.all():
                        if fila.fila_preferencial:
                            fila_preferencial = fila
                        else:
                            fila_normal = fila

                    for ficha in fila_normal.fichas.all():
                        if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                            permitido = False

                    for ficha in fila_preferencial.fichas.all():
                        if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                            permitido = False

                    if exame.agendamento and exame.agendamento.usuarios:
                        for user in exame.agendamento.usuarios.all():
                            if user == usuario[0]:
                                agendado = True

                    if permitido:

                        preferencial = None
                        
                        if request.POST.get('preferencial') == '0':
                            preferencial = False
                        else:
                            preferencial = True                        

                        if preferencial:
                            if fila_preferencial.vagas > 0:
                                ficha = Ficha()
                                ficha.numero = 0                                
                                ficha.preferencial = preferencial
                                ficha.usuario = usuario[0]
                                ficha.status = "AGUARDANDO"
                                ficha.excluida = False
                                ficha.save()

                                fila_preferencial.fichas.add(ficha)

                                gerarNumerosFichas(request, fila_preferencial)
                                
                                if agendado == False:
                                    fila_preferencial.vagas -= 1
                                    fila_normal.vagas -= 1

                                fila_preferencial.save()
                                fila_normal.save()
                                fichas = []
                                fichas.append(ficha)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                tmpJson = serializers.serialize("json", fichas)
                                tmpObj = json.loads(tmpJson)  
                                return HttpResponse(json.dumps(tmpObj))
                            else:
                                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)  

                        else:
                            if fila_normal.vagas > 0:
                                ficha = Ficha()
                                ficha.numero = 0                                
                                ficha.preferencial = preferencial
                                ficha.usuario = usuario[0]
                                ficha.status = "AGUARDANDO"
                                ficha.excluida = False
                                ficha.save()

                                fila_normal.fichas.add(ficha)

                                gerarNumerosFichas(request, fila_normal)

                                if agendado == False:
                                    fila_normal.vagas -= 1
                                    fila_preferencial.vagas -= 1

                                fila_normal.save()
                                fila_preferencial.save()
                                fichas = []
                                fichas.append(ficha)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                tmpJson = serializers.serialize("json", fichas)
                                tmpObj = json.loads(tmpJson)  
                                return HttpResponse(json.dumps(tmpObj))
                            else:
                                return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
                else:
                    return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

    @action(methods=['post'], detail=False)
    def desistir_ficha(self, request):
        token = request.POST.get('token')
        token = token.replace('"', '')
        
        if token:
            ficha = get_object_or_404(Ficha, pk=request.POST.get('id_ficha'))
            user = User.objects.filter(auth_token=token)
            usuario = Usuario.objects.filter(user=user[0])
            fila = Fila.objects.filter(fichas=ficha)
            consulta = Consulta.objects.get(filas=fila[0])

            if request.method == 'POST':

                if ficha.usuario == usuario[0]:
                    if fila[0].status != 'ENCERRADA':
                        ficha.status = "DESISTENTE"
                        ficha.excluida = True
                        ficha.save()

                        if fila[0].vagas < fila[0].total_fichas:
                            for fi in consulta.filas.all():
                                fi.vagas += 1
                                fi.save()
                        
                        gerarNumerosFichas(request, fila[0])
                        
                        #NOTIFICAÇÂO
                        nome = fila[0].nome
                        mensagem = 'Atenção, a fila: '+nome+' teve uma alteração, veja se a sua ficha mudou!'

                        if fila[0]:
                            if fila[0].fichas.all():
                                notificacoes.notificacaoColetiva(request, mensagem, fila[0].fichas.all())

                        return HttpResponse(status=status.HTTP_200_OK)
                    else:
                        ficha.excluida = True
                        ficha.save()

                        for fi in consulta.filas.all():
                            fi.vagas += 1
                            fi.save()

                        return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

        
# --------------------------FIM API--------------------------------------

@login_required(login_url='/accounts/login')
def printPDF(request):
    if has_permission(request.user, 'permissao_usuario'):
        html_string = render_to_string('printPDF.html', {'context': contexto.get()})
        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/ficha.pdf')
        fs = FileSystemStorage('/tmp')

        with fs.open('ficha.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="ficha.pdf'
        return response
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def cadastroFichaConsulta(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        consulta = get_object_or_404(Consulta, pk=id)
        usuario = Usuario.objects.filter(user=request.user)
        form = FormFicha(request.POST or None, request.FILES or None)
        permitido = True
        agendado = False
        fila_normal = None
        fila_preferencial = None

        if form.is_valid():
            if consulta.create_fila:
                
                for fila in consulta.filas.all():
                    if fila.fila_preferencial:
                        fila_preferencial = fila
                    else:
                        fila_normal = fila

                for ficha in fila_normal.fichas.all():
                    if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                        permitido = False

                for ficha in fila_preferencial.fichas.all():
                    if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                        permitido = False
                
                if consulta.agendamento:
                    if consulta.agendamento.usuarios.all():
                        for user in consulta.agendamento.usuarios.all():
                            if user == usuario[0]:
                                agendado = True

            if permitido:

                preferencial = form.cleaned_data['preferencial']

                if preferencial:
                    if fila_preferencial.vagas > 0:
                        ficha = Ficha()
                        ficha.numero = 0
                        ficha.preferencial = preferencial
                        ficha.usuario = usuario[0]
                        ficha.status = "AGUARDANDO"
                        ficha.excluida = False
                        ficha.save()

                        fila_preferencial.fichas.add(ficha)
                        
                        gerarNumerosFichas(fila_preferencial)
                        
                        if agendado == False:
                            fila_preferencial.vagas -= 1
                            fila_normal.vagas -= 1
                        fila_preferencial.save()
                        fila_normal.save()
                    else:
                        context = {
                            'form': form,
                            'msg_error': 'Essa fila não contém mais fichas disponíveis!'
                        }
                        return render(request, 'cadastro_ficha.html', {'context': context})
                else:
                    if fila_normal.vagas > 0:
                        ficha = Ficha()
                        ficha.numero = 0
                        ficha.preferencial = preferencial
                        ficha.usuario = usuario[0]
                        ficha.status = "AGUARDANDO"
                        ficha.excluida = False
                        ficha.save()

                        fila_normal.fichas.add(ficha)

                        gerarNumerosFichas(request, fila_normal)

                        if agendado == False:
                            fila_normal.vagas -= 1
                            fila_preferencial.vagas -= 1
                        fila_normal.save()
                        fila_preferencial.save()
                    else:
                        context = {
                            'form': form,
                            'msg_error': 'Essa fila não contém mais fichas disponíveis!'
                        }
                        return render(request, 'cadastro_ficha.html', {'context': context})

                return redirect('detalhesFicha', id=ficha.id)

            else:
                context = {
                    'form': form,
                    'msg_error': 'Você já está participando dessa fila!'
                }
                return render(request, 'cadastro_ficha.html', {'context': context})
        
        context = {
            'form': form,
        }

        return render(request, 'cadastro_ficha.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})    


@login_required(login_url='/accounts/login')
def cadastroFichaAutorizacao(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        usuario = Usuario.objects.filter(user=request.user) 
        form = FormFicha(request.POST or None, request.FILES or None)
        permitido = True
        agendado = False
        fila_normal = None
        fila_preferencial = None

        if form.is_valid():
            if autorizacao.create_fila:

                for fila in autorizacao.filas.all():
                    if fila.fila_preferencial:
                        fila_preferencial = fila
                    else:
                        fila_normal = fila

                for ficha in fila_normal.fichas.all():
                    if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                        permitido = False

                for ficha in fila_preferencial.fichas.all():
                    if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                        permitido = False
                
                if autorizacao.agendamento:
                    for user in autorizacao.agendamento.usuarios.all():
                        if user == usuario[0]:
                            agendado = True

            if permitido:
                preferencial = form.cleaned_data['preferencial']

                if preferencial:
                    if fila_preferencial.vagas > 0:
                        ficha = Ficha()
                        ficha.numero = 0
                        ficha.preferencial = preferencial
                        ficha.usuario = usuario[0]
                        ficha.status = "AGUARDANDO"
                        ficha.excluida = False
                        ficha.save()

                        fila_preferencial.fichas.add(ficha)

                        gerarNumerosFichas(request, fila_preferencial)

                        if agendado == False:
                            fila_preferencial.vagas -= 1
                            fila_normal.vagas -= 1
                        
                        fila_preferencial.save()
                        fila_normal.save()
                    else:
                        context = {
                            'form': form,
                            'msg_error': 'Essa fila não contém mais fichas disponíveis!'
                        }
                        return render(request, 'cadastro_ficha.html', {'context': context})
                else:
                    if fila_normal.vagas > 0:
                        ficha = Ficha()
                        ficha.numero = 0                            
                        ficha.preferencial = preferencial
                        ficha.usuario = usuario[0]
                        ficha.status = "AGUARDANDO"
                        ficha.excluida = False
                        ficha.save()

                        fila_normal.fichas.add(ficha)

                        gerarNumerosFichas(request, fila_normal)

                        if agendado == False:
                            fila_preferencial.vagas -= 1
                            fila_normal.vagas -= 1

                        fila_normal.save()
                        fila_preferencial.save()
                    else:
                        context = {
                            'form': form,
                            'msg_error': 'Essa fila não contém mais fichas disponíveis!'
                        }
                        return render(request, 'cadastro_ficha.html', {'context': context})

                return redirect('detalhesFicha', id=ficha.id)

            else:
                context = {
                    'form': form,
                    'msg_error': 'Você já está participando dessa fila!'
                }
                return render(request, 'cadastro_ficha.html', {'context': context})

        context = {
            'form': form,
        }

        return render(request, 'cadastro_ficha.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def cadastroFichaExame(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        exame = get_object_or_404(Exame, pk=id)
        usuario = Usuario.objects.filter(user=request.user) 
        form = FormFicha(request.POST or None, request.FILES or None)
        permitido = True
        agendado = False
        fila_normal = None
        fila_preferencial = None

        if form.is_valid():
            if exame.create_fila:

                for fila in exame.filas.all():
                    if fila.fila_preferencial:
                        fila_preferencial = fila
                    else:
                        fila_normal = fila

                for ficha in fila_normal.fichas.all():
                    if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                        permitido = False

                for ficha in fila_preferencial.fichas.all():
                    if ficha.usuario == usuario[0] and ficha.status != 'DESISTENTE':
                        permitido = False
                
                if exame.agendamento:
                    for user in exame.agendamento.usuarios.all():
                        if user == usuario[0]:
                            agendado = True

            if permitido:
                preferencial = form.cleaned_data['preferencial']

                if preferencial:
                    if fila_preferencial.vagas > 0:
                        ficha = Ficha()
                        ficha.numero = 0                            
                        ficha.preferencial = preferencial
                        ficha.usuario = usuario[0]
                        ficha.status = "AGUARDANDO"
                        ficha.excluida = False
                        ficha.save()

                        fila_preferencial.fichas.add(ficha)

                        gerarNumerosFichas(request, fila_preferencial)

                        if agendado == False:
                            fila_preferencial.vagas -= 1
                            fila_normal.vagas -= 1
                        
                        fila_preferencial.save()
                        fila_normal.save()
                    else:
                        context = {
                            'form': form,
                            'msg_error': 'Essa fila não contém mais fichas disponíveis!'
                        }
                        return render(request, 'cadastro_ficha.html', {'context': context})

                else:
                    if fila_normal.vagas > 0:
                        ficha = Ficha()
                        ficha.numero = 0                            
                        ficha.preferencial = preferencial
                        ficha.usuario = usuario[0]
                        ficha.status = "AGUARDANDO"
                        ficha.excluida = False
                        ficha.save()

                        fila_normal.fichas.add(ficha)

                        gerarNumerosFichas(request, fila_normal)

                        if agendado == False:
                            fila_preferencial.vagas -= 1
                            fila_normal.vagas -= 1

                        fila_normal.save()
                        fila_preferencial.save()
                    else:
                        context = {
                            'form': form,
                            'msg_error': 'Essa fila não contém mais fichas disponíveis!'
                        }
                        return render(request, 'cadastro_ficha.html', {'context': context})
                
                return redirect('detalhesFicha', id=ficha.id)

            else:
                context = {
                    'form': form,
                    'msg_error': 'Você já está participando dessa fila!'
                }
                return render(request, 'cadastro_ficha.html', {'context': context})

        context = {
            'form': form,
        }

        return render(request, 'cadastro_ficha.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def cadastroFichaAgendamento(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        agendamento = get_object_or_404(Agendamento, pk=id)
        form = FormFicha(request.POST or None, request.FILES or None)
        consulta = Consulta.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)

        if consulta:
            return redirect('cadastroFichaConsulta', id=consulta[0].id)
        elif autorizacao:
            return redirect('cadastroFichaAutorizacao', id=autorizacao[0].id)
        elif exame:
            return redirect('cadastroFichaExame', id=exame[0].id)
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})    

@login_required(login_url='/accounts/login')
def deleteFicha(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        ficha = get_object_or_404(Ficha, pk=id)
        usuario = Usuario.objects.filter(user=request.user)
        fila = Fila.objects.get(fichas=ficha)
        consulta = Consulta.objects.get(filas=fila)

        if request.method == 'POST':
            context = {}
            
            if ficha.usuario == usuario[0]:
                if fila.status != 'ENCERRADA':
                    ficha.status = 'DESISTENTE'
                    ficha.excluida = True
                    ficha.save()

                    if fila.vagas < fila.total_fichas:
                        for fi in consulta.filas.all():
                            fi.vagas += 1
                            fi.save()
                    
                    gerarNumerosFichas(request, fila)

                    #NOTIFICAÇÂO
                    mensagem = 'Atenção, a fila: '+ fila.nome + ' teve uma alteração, veja se a sua ficha mudou!'

                    if fila:
                        if fila.fichas.all():
                            notificacoes.notificacaoColetiva(request, mensagem, fila.fichas.all())

                    context['msg_alert'] = 'Exclusão realizada com sucesso'

                else:
                    ficha.excluida = True
                    ficha.save()

                    for fi in consulta.filas.all():
                        fi.vagas += 1
                        fi.save()
                    
                    context['msg_alert'] = 'Exclusão realizada com sucesso'
            else:
                context['msg_error'] = 'Você não participa dessa fila'

            return render(request, 'home_usuario.html', {'context': context})

        return render(request, 'delete_ficha.html', {'ficha': ficha})
    else:
        context['msg_error'] = 'Impossivel Acessar Essa Área'

        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def detalhesFicha(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        ficha = get_object_or_404(Ficha, pk=id)
        filas = Fila.objects.filter(fichas=ficha)
        usuario = ficha.usuario
        fila_preferencial = None
        fila_normal = None
        unidade_aux = None

        for fila in filas.all():
            if fila.fila_preferencial:
                fila_preferencial = fila
            else:
                fila_normal = fila

        if fila_preferencial:

            consulta = Consulta.objects.filter(filas=fila_preferencial)
            autorizacao = Autorizacao.objects.filter(filas=fila_preferencial)
            exame = Exame.objects.filter(filas=fila_preferencial)

            if consulta:
                unidade = UnidadeSaude.objects.get(consultas=consulta[0])
                unidade_aux = unidade[0]


            elif autorizacao:
                unidade = UnidadeSaude.objects.get(autorizacoes=autorizacao[0])
                unidade_aux = unidade[0]
            
            elif exame:
                unidade = UnidadeSaude.objects.get(autorizacoes=autorizacao[0])
                unidade_aux = unidade[0]

            context = {
                'ficha': ficha,
                'fila_preferencial': fila_preferencial,
                'usuario': usuario,
                'unidade': unidade_aux
            }
        else:
            consulta = Consulta.objects.filter(filas=fila_normal)
            autorizacao = Autorizacao.objects.filter(filas=fila_normal)
            exame = Exame.objects.filter(filas=fila_normal)

            if consulta:
                unidade = UnidadeSaude.objects.filter(consultas=consulta[0])
                unidade_aux = unidade[0]

            elif autorizacao:
                unidade = UnidadeSaude.objects.filter(autorizacoes=autorizacao[0])
                unidade_aux = unidade[0]
            
            elif exame:
                unidade = UnidadeSaude.objects.get(autorizacoes=autorizacao[0])
                unidade_aux = unidade[0]

            context = {
                'ficha': ficha,
                'fila_normal': fila_normal,
                'usuario': usuario,
                'unidade': unidade_aux
            }

        contexto.set(context)

        return render(request, 'detalhes_ficha.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

def gerarNumerosFichas(request, fila):
    num = 1
    for ficha in fila.fichas.all():
        if ficha.status != 'DESISTENTE':
            ficha.numero = num
            ficha.save()
            num += 1


class Context(object):
    def __init__(self, context):
        self.__context = context
    
    def get(self):
        return self.__context

    def set(self, context):
        self.__context = context

contexto = Context(None)



