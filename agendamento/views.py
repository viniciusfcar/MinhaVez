from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Agendamento
from .forms import FormAgendamento
from usuario.models import Usuario
from autorizacao.models import Autorizacao
from consulta.models import Consulta
from exame.models import Exame
from unidadeSaude.models import UnidadeSaude
from especialista.models import Especialista
from responsavel.models import Responsavel
from rolepermissions.checkers import has_permission
from rest_framework import viewsets
from .serializers import AgendamentoSerializer
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from notificacoes import views as notificacoes
from datetime import date, datetime


class GetAgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        queryset = Agendamento.objects.all()
        return queryset

    @action(methods=['get'], detail=True)
    def agendamento_usuario(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        agendamentos = Agendamento.objects.filter(usuarios=usuario)
        tmpJson = serializers.serialize("json", agendamentos)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

    @action(methods=['get'], detail=True)
    def detalhes_agendamento(self, request, pk=None):
        agendamento = get_object_or_404(Agendamento, pk=pk)
        consulta = Consulta.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)
        aux = None
        if consulta:
            aux = consulta
        elif autorizacao:
            aux = autorizacao
        else:
            aux = exame
            
        tmpJson = serializers.serialize("json", aux)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

@login_required(login_url='/accounts/login')
def cadastroAgendamentoConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)

        if request.method == 'POST':

            agendamento = Agendamento(nome=request.POST.get('nome'), vagas=request.POST.get('vagas'))
            agendamento.save()
            consulta.agendamento = agendamento
            consulta.verifica = True
            consulta.save()
            return redirect('detalhesAgendamento', id=agendamento.id)
        else:
            form = FormAgendamento()

        context = {
            'consulta': consulta,
            'form': form,
        }

    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('homeUsuario', {'context': context})

    return render(request, 'cadastro_agendamento_consulta.html', {'context': context})

@login_required(login_url='/accounts/login')
def cadastroAgendamentoAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)

        if request.method == 'POST':

            agendamento = Agendamento(nome=request.POST.get('nome'), vagas=request.POST.get('vagas'))
            agendamento.save()
            autorizacao.agendamento = agendamento
            autorizacao.verifica = True
            autorizacao.save()
            return redirect('detalhesAgendamento', id=agendamento.id)
        else:
            form = FormAgendamento()

        context = {
            'autorizacao': autorizacao,
            'form': form,
        }

    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('homeUsuario', {'context': context})

    return render(request, 'cadastro_agendamento_autorizacao.html', {'context': context})

@login_required(login_url='/accounts/login')
def cadastroAgendamentoExame(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        exame = get_object_or_404(Exame, pk=id)

        if request.method == 'POST':

            agendamento = Agendamento(nome=request.POST.get('nome'), vagas=request.POST.get('vagas'))
            agendamento.save()
            exame.agendamento = agendamento
            exame.verifica = True
            exame.save()
            return redirect('detalhesAgendamento', id=agendamento.id)
        else:
            form = FormAgendamento()

        context = {
            'exame': exame,
            'form': form,
        }

    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('homeUsuario', {'context': context})

    return render(request, 'cadastro_agendamento_exame.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaAgendamento(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        especialistas = unidade[0].especialistas.all()
        responsaveis = unidade[0].responsaveis.all()

        data_today = date.today()

        context = {
            'especialistas': especialistas,
            'responsaveis': responsaveis
        }

        if unidade:
            if request.method == 'POST':

                esp = request.POST.get('especialista', None)
                resp = request.POST.get('responsavel', None)
                ex = request.POST.get('exames', None)

                exames = None

                data = request.POST.get('data', None)
                dataFinal = request.POST.get('dataFinal', None)

                if esp:
                    esp = Especialista.objects.get(id=esp)
                
                if resp:
                    resp = Responsavel.objects.get(id=resp)
                
                if ex:
                    exames = unidade[0].exames.all().filter(agendamento__isnull=False).order_by('data', 'hora')
                
                consultas = unidade[0].consultas.all().filter(especialista=esp).filter(agendamento__isnull=False).order_by('data', 'hora')
                autorizacoes = unidade[0].autorizacoes.all().filter(responsavel=resp).filter(agendamento__isnull=False).order_by('data', 'hora')
                
                if consultas:
                    consultas_aux = consultas = unidade[0].consultas.all().extra(where=['status <> "ENCERRADA"']).filter(especialista=esp).filter(agendamento__isnull=False).order_by('data', 'hora')
                    
                    context = {
                        'especialistas': especialistas,
                        'responsaveis': responsaveis,
                        'especialista': esp,
                        'data': data_today,
                    }

                    if consultas_aux:
                        context['objetos'] = consultas_aux
                    
                    elif not consultas_aux:
                        context['msg_alert2'] = 'Não possui Agendamentos em aguardo ou iniciados!'

                    if data:
                        consultas_aux = unidade[0].consultas.filter(especialista=esp, data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')], agendamento__isnull=False).order_by('data', 'hora')
    
                        if consultas_aux:
                            context['objetos'] = consultas_aux
                            context['msg_alert2'] = None
                        else:
                            context['msg_busca'] = 'Nada encontrado para esses parâmetros!'

                elif autorizacoes:
                    autorizacoes_aux = unidade[0].autorizacoes.all().extra(where=['status <> "ENCERRADA"']).filter(responsavel=resp).filter(agendamento__isnull=False).order_by('data', 'hora')
                    
                    context = {
                        'especialistas': especialistas,
                        'responsaveis': responsaveis,
                        'responsavel': resp,
                        'data': data_today,
                    }

                    if autorizacoes_aux:
                        context['objetos'] = autorizacoes_aux
                    
                    elif not autorizacoes_aux:
                        context['msg_alert2'] = 'Não possui Agendamentos em aguardo ou iniciados!'

                    if data:
                        autorizacoes_aux = unidade[0].autorizacoes.filter(responsavel=resp, data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')], agendamento__isnull=False).order_by('data', 'hora')

                        if autorizacoes_aux:
                            context['objetos'] = autorizacoes_aux
                            context['msg_alert2'] = None
                        else:
                            context['msg_busca'] = 'Nada encontrado para esses parâmetros!'
                
                elif exames:
                    exames_aux = unidade[0].exames.all().extra(where=['status <> "ENCERRADA"']).filter(agendamento__isnull=False).order_by('data', 'hora')
                    
                    context = {
                        'especialistas': especialistas,
                        'responsaveis': responsaveis,
                        'responsavel': resp,
                        'data': data_today,
                        'exames': ex
                    }

                    if exames_aux:
                        context['objetos'] = exames_aux
                    
                    elif not exames_aux:
                        context['msg_alert2'] = 'Não possui Agendamentos em aguardo ou iniciados!'

                    if data:
                        exames_aux = unidade[0].exames.filter(data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')], agendamento__isnull=False).order_by('data', 'hora')

                        if autorizacoes_aux:
                            context['objetos'] = autorizacoes_aux
                            context['msg_alert2'] = None
                        else:
                            context['msg_busca'] = 'Nada encontrado para esses parâmetros!'
                else:
                    context = {
                        'especialistas': especialistas,
                        'responsaveis': responsaveis,
                        'especialista': esp,
                        'responsavel': resp,
                        'msg_alert': 'Não possui Agendamentos!',
                        'data': data_today,
                    }

                contexto.set(context)
            return render(request, 'lista_agendamento.html', {'context': context})

        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def deleteAgendamento(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        agendamento = get_object_or_404(Agendamento, pk=id)
        consulta = Consulta.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)

        if request.method == 'POST':
            if consulta:
                if consulta[0].user == request.user:
                    agendamento.delete()
                    return redirect('detalhesConsulta', id=consulta[0].id)
                else:
                    context = {
                        'msg_error': 'Indisponivel Acessar Essa Área'
                    }

                    return redirect('homeUnidadeSaude', {'context': context})
            
            elif autorizacao:
                if autorizacao[0].user == request.user:
                    agendamento.delete()
                    return redirect('detalhesAutorizacao', id=autorizacao[0].id)
            
            elif exame:
                if exame[0].user == request.user:
                    agendamento.delete()
                    return redirect('detalhesExame', id=exame[0].id)

        return render(request, 'delete_agendamento.html', {'agendamento': agendamento})
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'
        }

        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def detalhesAgendamento(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        agendamento = get_object_or_404(Agendamento, pk=id)
        usuarios = agendamento.usuarios
        consulta = Consulta.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)
        data = date.today()
    
        if consulta:
            context = {
                'agendamento': agendamento,
                'usuarios': usuarios,
                'consulta': consulta[0],
                'data': data
            }
        elif autorizacao:
            context = {
                'agendamento': agendamento,
                'usuarios': usuarios,
                'autorizacao': autorizacao[0],
                'data': data
            }
        elif exame:
            context = {
                'agendamento': agendamento,
                'usuarios': usuarios,
                'exame': exame[0],
                'data': data
            }

        contexto.set(context)

        return render(request, 'detalhes_agendamento.html', {'context': context})
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'
        }

        return render(request, 'home_usuario.html', {'context': context})

    return render(request, 'detalhes_agendamento.html', {'context': context})


@login_required(login_url='/accounts/login')
def adicionaUsuarioAgendamento(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        agendamento = get_object_or_404(Agendamento, pk=id)
        consulta = Consulta.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)

        if consulta:
            context = {
                'agendamento': agendamento,
                'usuarios': agendamento.usuarios,
                'consulta': consulta[0],
            }
        
        if autorizacao:
            context = {
                'agendamento': agendamento,
                'usuarios': agendamento.usuarios,
                'autorizacao': autorizacao[0],
            }

        if exame:
            context = {
                'agendamento': agendamento,
                'usuarios': agendamento.usuarios,
                'exame': exame[0],
            }

        if request.method == 'POST':
            
            cpf = request.POST.get('cpf')
            sus = request.POST.get('sus')

            if cpf:
                try:
                    usuario = Usuario.objects.get(cpf=cpf)
                except:
                    usuario = None

            if sus:
                try:
                    usuario = Usuario.objects.get(sus=sus)
                except:
                    usuario = None
                    
            na_fila = False

            for user in agendamento.usuarios.all():
                if user == usuario:
                    na_fila = True

            if usuario and na_fila == False:
                if agendamento.vagas > 0:
                    agendamento.usuarios.add(usuario)
                    agendamento.vagas -= 1
                    agendamento.save()
                    
                else:
                    context['msg_vagas'] = 'Vagas excedidas.'
            else:
                context['msg_usuario'] = 'Usuário não localizado ou já está nesse agendamento.'

            #NOTIFICAÇÂO
            if usuario:
                mensagem = usuario.user.first_name+' você foi adicionado no agendamento: '+agendamento.nome+'. Verifique os detalhes para mais informações !'
                notificacoes.notificacaoIndividual(request, mensagem, usuario)
            
            return render(request, 'detalhes_agendamento.html', {'context': context})
            
        return render(request, 'detalhes_agendamento.html', {'context': context})
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def excluiUsuarioAgendamento(request, idUser, id):
    if has_permission(request.user, 'permissao_unidade'):
        agendamento = get_object_or_404(Agendamento, pk=id)
        usuario = get_object_or_404(Usuario, pk=idUser)
        consulta = Consulta.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)

        if request.method == 'POST':
            if consulta:
                if usuario:
                    agendamento.usuarios.remove(usuario)
                    agendamento.vagas += 1
                    agendamento.save()

            elif autorizacao:
                if usuario:
                    agendamento.usuarios.remove(usuario)
                    agendamento.vagas += 1
                    agendamento.save()
            
            elif exame:
                if usuario:
                    agendamento.usuarios.remove(usuario)
                    agendamento.vagas += 1
                    agendamento.save()
            
            #NOTIFICAÇÂO
            mensagem = usuario.user.first_name+' você foi excluido do agendamento: '+agendamento.nome+'. Para mais informações entre em contato com a Unidade de Saúde!'
            notificacoes.notificacaoIndividual(request, mensagem, usuario)

            return redirect('detalhesAgendamento', id=agendamento.id)

        context = {
            'agendamento': agendamento,
            'usuarios': agendamento.usuarios,
            'usuario': usuario,
        }

        return render(request, 'exclui_usuario_agendamento.html', {'context': context})
    else:
        context = {
            'msg_error': 'Indisponivel Acessar Essa Área'
        }

@login_required(login_url='/accounts/login')
def detalhesAgendamentoUsuario(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        agendamento = get_object_or_404(Agendamento, pk=id)
        consulta = Consulta.objects.filter(agendamento=agendamento)
        autorizacao = Autorizacao.objects.filter(agendamento=agendamento)
        exame = Exame.objects.filter(agendamento=agendamento)
        
        if consulta:
            context = {
                'agendamento': agendamento,
                'consulta': consulta[0],
            }
        elif autorizacao:
            context = {
                'agendamento': agendamento,
                'autorizacao': autorizacao[0],
            }
        
        elif exame:
            context = {
                'agendamento': agendamento,
                'exame': exame[0],
            }
        return render(request, 'detalhes_agendamento_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acesssar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioAgendamento(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_agendamento.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_agendamento.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_agendamento.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_agendamento.pdf'
        return response
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioListaAgendamento(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_lista_agendamento.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_lista_agendamentos.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_lista_agendamentos.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_lista_agendamentos.pdf'
        return response
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


class Context(object):
    def __init__(self, context):
        self.__context = context
    
    def get(self):
        return self.__context

    def set(self, context):
        self.__context = context

contexto = Context(None)

