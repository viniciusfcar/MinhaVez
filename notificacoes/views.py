from django.shortcuts import render, redirect, get_object_or_404
import onesignal as onesignal_sdk
import requests
import json
from usuario.models import Usuario
from django.contrib.auth.models import User
from consulta.models import Consulta
from agendamento.models import Agendamento
from datetime import date
from .models import Notificacao
from rest_framework import viewsets
from .serializers import NotificacaoSerializer
from django.contrib.auth.decorators import login_required
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action
from rest_framework import status
from django.http import HttpResponse, JsonResponse

class GetNotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer

    def get_queryset(self):
        queryset = Notificacao.objects.all().order_by('status')
        return queryset

    @action(methods=['post'], detail=False)
    def ler_notificacao(self, request):
        idNot = request.POST.get('idNotificacao')
        notificacao = get_object_or_404(Notificacao, pk=idNot)
        token = request.POST.get('token')
        token = token.replace('"', '')
        user = User.objects.filter(auth_token=token)
        usuario = Usuario.objects.filter(user=user[0])

        if request.method == 'POST':
            if usuario:
                if notificacao:
                    notificacao.status = True
                    notificacao.save()
                    usuario[0].save()
                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=False)
    def delete_notificacao(self, request):
        idNot = request.POST.get('idNotificacao')
        notificacao = get_object_or_404(Notificacao, pk=idNot)
        token = request.POST.get('token')
        token = token.replace('"', '')
        user = User.objects.filter(auth_token=token)
        usuario = Usuario.objects.filter(user=user[0])

        if request.method == 'POST':
            if usuario:
                if notificacao:
                    usuario[0].notificacoes.remove(notificacao)
                    notificacao.delete()
                    usuario[0].save()
                    return HttpResponse(status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def inicioConsultaAutorizacao(request, mensagem, objeto):
    
    fila_normal = None
    fila_preferencial = None
    ids = []

    notificacao = Notificacao(titulo='Fique Atento!', assunto=mensagem)
    notificacao.save()

    for fila in objeto.filas.all():
        if fila.fila_preferencial:
            fila_preferencial = fila
        else:
            fila_normal = fila
    
    for ficha in fila_normal.fichas.all():
        if ficha.status != 'DESISTENTE':
            ids.append(ficha.usuario.notificacao)
            ficha.usuario.notificacoes.add(notificacao)
            ficha.usuario.save()
    
    for ficha in fila_preferencial.fichas.all():
        if ficha.status != 'DESISTENTE':
            ids.append(ficha.usuario.notificacao)
            ficha.usuario.notificacoes.add(notificacao)
            ficha.usuario.save()

    header = {"Content-Type": "application/json; charset=utf-8",
        "Authorization": "Basic AAAAYp3wnKU:APA91bF6BbpMdRc6-wvAbfdf76ItATkG9EBz2uDa2BIDWyFYP4tcSU1EgE6pnC-2QbD4sgFvS5_96TDpglzdsD09QTIi9e4lmxOxGfgiJlDwpP-54GEpW_j3tYTcuo7NF9N3Z2IRJvmK"}

    payload = {"app_id": "0414c64c-3f63-486a-8fa2-78ce89f5032e",
            "include_player_ids": ids,
            "headings": {"en": "MinhaVez"},
            "contents": {"en": mensagem}}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

def avisaPosicaoFila(request, objeto):
    fichas_restante = 0

    for ficha in objeto.fichas.all():
        if ficha.status == 'AGUARDANDO':
            if fichas_restante == 0:
                mensagem = ficha.usuario.user.first_name+' é a sua vez, esteja pronto(a)!'

                notificacao = Notificacao(titulo='Posição na Fila!', assunto=mensagem)
                notificacao.save()
                
                header = {"Content-Type": "application/json; charset=utf-8",
                    "Authorization": "Basic AAAAYp3wnKU:APA91bF6BbpMdRc6-wvAbfdf76ItATkG9EBz2uDa2BIDWyFYP4tcSU1EgE6pnC-2QbD4sgFvS5_96TDpglzdsD09QTIi9e4lmxOxGfgiJlDwpP-54GEpW_j3tYTcuo7NF9N3Z2IRJvmK"}

                payload = {"app_id": "0414c64c-3f63-486a-8fa2-78ce89f5032e",
                        "include_player_ids": [ficha.usuario.notificacao],
                        "headings": {"en": "MinhaVez"},
                        "contents": {"en": mensagem}}
                
                req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

                ficha.usuario.notificacoes.add(notificacao)
                ficha.usuario.save()

                fichas_restante += 1
            else:
                mensagem = "Faltam "+str(fichas_restante)+" ficha(s) para que você seja atendido, fique atento(a) "+ficha.usuario.user.first_name+"!"

                notificacao = Notificacao(titulo='Posição na Fila!', assunto=mensagem)
                notificacao.save()

                header = {"Content-Type": "application/json; charset=utf-8",
                    "Authorization": "Basic AAAAYp3wnKU:APA91bF6BbpMdRc6-wvAbfdf76ItATkG9EBz2uDa2BIDWyFYP4tcSU1EgE6pnC-2QbD4sgFvS5_96TDpglzdsD09QTIi9e4lmxOxGfgiJlDwpP-54GEpW_j3tYTcuo7NF9N3Z2IRJvmK"}

                payload = {"app_id": "0414c64c-3f63-486a-8fa2-78ce89f5032e",
                        "include_player_ids": [ficha.usuario.notificacao],
                        "headings": {"en": "MinhaVez"},
                        "contents": {"en": mensagem}}
                
                req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

                ficha.usuario.notificacoes.add(notificacao)
                ficha.usuario.save()
                
                fichas_restante += 1

def notificacaoIndividual(request, mensagem, usuario):
    
    notificacao = Notificacao(titulo='Fique de olho!', assunto=mensagem)
    notificacao.save()

    header = {"Content-Type": "application/json; charset=utf-8",
        "Authorization": "Basic AAAAYp3wnKU:APA91bF6BbpMdRc6-wvAbfdf76ItATkG9EBz2uDa2BIDWyFYP4tcSU1EgE6pnC-2QbD4sgFvS5_96TDpglzdsD09QTIi9e4lmxOxGfgiJlDwpP-54GEpW_j3tYTcuo7NF9N3Z2IRJvmK"}

    payload = {"app_id": "0414c64c-3f63-486a-8fa2-78ce89f5032e",
            "include_player_ids": [usuario.notificacao],
            "headings": {"en": "MinhaVez"},
            "contents": {"en": mensagem}}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

    usuario.notificacoes.add(notificacao)
    usuario.save()


def notificacaoColetiva(request, mensagem, objeto):
    for obj in objeto:
        notificacaoIndividual(request, mensagem, obj.usuario)
    

def notificacaoAgendamento(request, mensagem, objeto):
    for usuario in objeto.usuarios.all():
        notificacaoIndividual(request, mensagem, usuario)

@login_required(login_url='/accounts/login')
def listaNotificacoes(request):
    if has_permission(request.user, 'permissao_usuario'):
        usuario = Usuario.objects.filter(user=request.user)
        notificacoes = usuario[0].notificacoes.all().order_by('status')

        if notificacoes:

            context = {
                'notificacoes': notificacoes
            }

            return render(request, 'lista_notificacoes.html', {'context': context})
        else:

            context = {
                'msg': 'Nenhuma notificação até o momento'
            }

            return render(request, 'lista_notificacoes.html', {'context': context})
    
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

def lerNotificacao(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        notificacao = get_object_or_404(Notificacao, pk=id)

        if request.method == 'POST':
            if notificacao.status == False:
                notificacao.status = True
                notificacao.save()
                return redirect('listaNotificacoes')
            else:
                pass
        else:
            pass
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

def deleteNotificacao(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        notificacao = get_object_or_404(Notificacao, pk=id)
        usuario = Usuario.objects.filter(notificacoes=notificacao)

        if request.method == 'POST':
            usuario[0].notificacoes.remove(notificacao)
            notificacao.delete()
            return redirect('listaNotificacoes')
        else:
            pass
        
        return render(request, 'delete_notificacao.html', {'notificacao': notificacao})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})
                
