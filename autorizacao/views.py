from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FormAutorizacao
from unidadeSaude.models import UnidadeSaude
from .models import Autorizacao
from ficha.models import Ficha
from fila.models import Fila
from rest_framework import viewsets
from .serializers import AutorizacaoSerializer
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from responsavel.models import Responsavel
from datetime import date, datetime
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework.filters import SearchFilter
from notificacoes import views as notificacoes
from rest_framework import status
from datetime import date

class GetAutorizacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AutorizacaoSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^nome', '^data', '^status', '^responsavel__nome')

    def get_queryset(self):
        queryset = Autorizacao.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
        return queryset

    @action(methods=['get'], detail=True)
    def autorizacao_ficha(self, request, pk=None):
        ficha = get_object_or_404(Ficha, pk=pk)
        filas = Fila.objects.filter(fichas=ficha)
        autorizacao = Autorizacao.objects.filter(filas=filas[0])
        tmpJson = serializers.serialize("json", autorizacao)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))
    
    @action(methods=['get'], detail=True)
    def get_status_autorizacao(self, request, pk=None):
        autorizacao = get_object_or_404(Autorizacao, pk=pk)

        if autorizacao.status == 'INICIADA':
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@login_required(login_url='/accounts/login')
def cadastroAutorizacao(request):
    if has_permission(request.user, 'permissao_unidade'):
        form = FormAutorizacao(request.POST or None, request.FILES or None)

        if request.method == 'POST':

            try:
                datetime.strptime(request.POST.get('hora'), '%H:%M')
                datetime.strptime(request.POST.get('data'), '%Y-%m-%d')

                resp = Responsavel.objects.get(id=request.POST.get('responsavel'))

                autorizacao = Autorizacao(nome=request.POST.get('nome'), data=request.POST.get('data'), hora=request.POST.get('hora'))

                autorizacao.responsavel = resp
                autorizacao.user = request.user
                autorizacao.create_fila = False
                autorizacao.status = "AGUARDANDO"
                autorizacao.save()
                unidade = UnidadeSaude.objects.filter(users=request.user)
                if unidade:
                    unidade[0].autorizacoes.add(autorizacao)
                    unidade[0].save()

                return redirect('listaAutorizacao')
            
            except ValueError:
                unidade = UnidadeSaude.objects.filter(users=request.user)
                context = {
                    'responsaveis': unidade[0].responsaveis.all
                }

                return render(request, 'cadastro_autorizacao.html', {'context': context})
        
        unidade = UnidadeSaude.objects.filter(users=request.user)
        context = {
            'responsaveis': unidade[0].responsaveis.all
        }

        return render(request, 'cadastro_autorizacao.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaAutorizacao(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        pesquisa = request.GET.get('pesquisa', None)
        data = request.GET.get('data', None)
        dataFinal = request.GET.get('dataFinal', None)
        data_rel = date.today()

        if unidade:
            autorizacoes = unidade[0].autorizacoes.all().extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-create_fila', '-status')
            
            context = {
                'data': data_rel
            }

            if autorizacoes:
                context['autorizacoes'] = autorizacoes

            if pesquisa:
                resp = Responsavel.objects.filter(nome__icontains=pesquisa)

                if resp:
                    
                    autorizacoes_aux = unidade[0].autorizacoes.filter(nome__icontains=pesquisa) | autorizacoes.filter(status__icontains=pesquisa) | autorizacoes.filter(responsavel__nome=resp[0])
                    
                    if autorizacoes_aux:
                        context['autorizacoes'] = autorizacoes_aux
                    
                    else:
                        context['msg_busca'] = 'Nada encontrado para esses parâmetros!'
                else:
                    autorizacoes_aux = unidade[0].autorizacoes.filter(nome__icontains=pesquisa) | autorizacoes.filter(status__icontains=pesquisa)
                    
                    if autorizacoes_aux:
                        context['autorizacoes'] = autorizacoes_aux
                    else:
                        context['msg_busca'] = 'Nada encontrado para esses parâmetros!'

            if data:
                try:
                    autorizacoes_aux = unidade[0].autorizacoes.filter(data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')]).order_by('data', 'hora', '-create_fila')
                    
                    if autorizacoes_aux:
                        context['autorizacoes'] = autorizacoes_aux
                    
                    else:
                        context['msg_busca'] = 'Nada encontrado para esses parâmetros!'

                except ValueError:
                    context['msg_busca'] = 'Informe uma data válida!'

            if not autorizacoes:
                autorizacoes_aux = unidade[0].autorizacoes.all()

                if autorizacoes_aux:
                    context['msg_alert'] = 'Nenhuma Autorização em aguardo!'
                
                else:
                    context['msg_alert'] = 'Nenhuma Autorização cadastrada!'

            contexto.set(context)
            
            return render(request, 'lista_autorizacao.html', {'context': context})

        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }

            return render(request, 'home.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def alterarAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        unidade = UnidadeSaude.objects.filter(users=request.user)
        fila_normal = None
        fila_preferencial = None

        if autorizacao.filas.all():
            for fila in autorizacao.filas.all():
                if fila.fila_preferencial:
                    fila_preferencial = fila
                else:
                    fila_normal = fila

        if request.method == 'POST':
            if autorizacao.user == request.user:
                try:
                    datetime.strptime(request.POST.get('hora'), '%H:%M')
                    datetime.strptime(request.POST.get('data'), '%Y-%m-%d')

                    resp = Responsavel.objects.get(id=request.POST.get('responsavel'))

                    autorizacao.hora = request.POST.get('hora')
                    autorizacao.data = request.POST.get('data')
                    autorizacao.responsavel = resp
                    autorizacao.nome = request.POST.get('nome')

                    autorizacao.save()
                    
                    #NOTIFICAÇÂO
                    mensagem = 'Atenção, a autorização: '+ autorizacao.nome + ' teve uma alteração, fique atento!'

                    if fila_normal:
                        if fila_normal.fichas.all():
                            notificacoes.notificacaoColetiva(request, mensagem, fila_normal.fichas.all())
                    
                    if fila_preferencial:
                        if fila_preferencial.fichas.all():
                            notificacoes.notificacaoColetiva(request, mensagem, fila_preferencial.fichas.all())
                    
                    if autorizacao.agendamento:
                        if autorizacao.agendamento.usuarios.all():
                            notificacoes.notificacaoAgendamento(request, mensagem, autorizacao.agendamento)
                    
                    return redirect('listaAutorizacao')
                
                except ValueError:
                    context = {
                        'autorizacao': autorizacao,
                    }

                    return render(request, 'cadastro_autorizacao.html', {'context': context})

            elif autorizacao.user != request.user:
                context = {
                    'msg_error': 'Indisponivel Acessar Essa Área'

                }
                return redirect('homeUnidadeSaude', {'context': context})

        context = {
            'autorizacao': autorizacao,
            'responsaveis': unidade[0].responsaveis.all
        }

        return render(request, 'cadastro_autorizacao.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def deleteAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        fila_normal = None
        fila_preferencial = None
        agendamento = autorizacao.agendamento

        for fila in autorizacao.filas.all():
            if fila.fila_preferencial:
                fila_preferencial = fila
            else:
                fila_normal = fila

        if autorizacao.user == request.user:
            if request.method == 'POST':
                
                if fila_normal != None:
                    fila_normal.delete()
                    fila_preferencial.delete()
                
                if agendamento != None:
                    agendamento.delete()

                autorizacao.delete()
                return redirect('listaAutorizacao')
        elif autorizacao.user != request.user:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'

            }
            return redirect('homeUnidadeSaude', {'context': context})

        return render(request, 'delete_autorizacao.html', {'nome': autorizacao.nome})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def detalhesAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        fila_normal = None
        fila_preferencial = None
        fichas_normais = [None]
        fichas_preferenciais = [None]
        data = date.today()

        for fila in autorizacao.filas.all():
            if fila.fila_preferencial:
                fila_preferencial = fila
            else:
                fila_normal = fila
                
        if fila_normal:
            for ficha in fila_normal.fichas.all():
                fichas_normais.append(ficha)
        
        if fila_preferencial:
            for ficha in fila_preferencial.fichas.all():
                fichas_preferenciais.append(ficha)

        context = {
            'autorizacao': autorizacao,
            'fila_preferencial': fila_preferencial,
            'fila_normal': fila_normal,
            'fichas_normais': fichas_normais,
            'fichas_preferenciais': fichas_preferenciais,
            'data': data
        }

        contexto.set(context)

        return render(request, 'detalhes_autorizacao.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaAutorizacaoUsuario(request):
    if has_permission(request.user, 'permissao_usuario'):
        autorizacoes = Autorizacao.objects.all().order_by('hora', '-data', '-create_fila', '-status')
        pesquisa = request.GET.get('pesquisa')
        resp = Responsavel.objects.filter(nome=request.GET.get('pesquisa', None))
        data = request.GET.get('data', None)

        if resp:
            autorizacoes = autorizacoes.filter(responsavel__icontains=resp[0]).order_by('hora', 'data', '-create_fila') | autorizacoes.filter(nome__icontains=pesquisa).order_by('hora', 'data', '-create_fila') | autorizacoes.filter(status__icontains=pesquisa).order_by('hora', 'data', '-create_fila')
            if autorizacoes:
                context = {
                    'autorizacoes': autorizacoes
                }
            else:
                autorizacoes = Autorizacao.objects.all().order_by('hora', '-data', '-create_fila', '-status')
                context = {
                    'autorizacoes': autorizacoes,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif data:
            try:
                datetime.strptime(data, '%Y-%m-%d')

                autorizacoes = autorizacoes.filter(data=data).order_by('hora', '-data', '-create_fila', '-status')
                if autorizacoes:
                    context = {
                        'autorizacoes': autorizacoes
                    }
                else:
                    autorizacoes = Autorizacao.objects.all().order_by('hora', '-data', '-create_fila', '-status')
                    context = {
                        'autorizacoes': autorizacoes,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }

            except ValueError:
                autorizacoes = Autorizacao.objects.all().order_by('hora', '-data', '-create_fila', '-status')
                context = {
                    'autorizacoes': autorizacoes,
                    'msg_busca': 'Informe uma data válida!'
                }

        elif pesquisa:
            autorizacoes = autorizacoes.filter(nome__icontains=pesquisa).order_by('hora', '-data', '-create_fila') | autorizacoes.filter(status__icontains=pesquisa).order_by('hora', 'data', 'create_fila')
            if autorizacoes:
                context = {
                    'autorizacoes': autorizacoes
                }
            else:
                autorizacoes = Autorizacao.objects.all().order_by('hora', '-data', '-create_fila', '-status')
                context = {
                    'autorizacoes': autorizacoes,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif autorizacoes:
            context = {
                'autorizacoes': autorizacoes
            }
        else:
            context = {
                'msg_error': 'Nenhuma autorização cadastrada!'
            }

        return render(request, 'lista_autorizacao_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def iniciarAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        fila_normal = None
        fila_preferencial = None

        if autorizacao.filas.all():
            for fila in autorizacao.filas.all():
                if fila.fila_preferencial:
                    fila_preferencial = fila
                else:
                    fila_normal = fila
            
            autorizacao.status = "INICIADA"
            autorizacao.save()

            if autorizacao.filas.all():
                if fila_normal.fichas.all() or fila_preferencial.fichas.all():
                    #PARTE DO ENVIO DA NOTIFICACAO
                    mensagem = "A autorização: " + autorizacao.nome + " foi iniciada, fique atento para não perder a sua vez!"
                    notificacoes.inicioConsultaAutorizacao(request, mensagem, autorizacao)

            context = {
                'autorizacao': autorizacao,
                'fila_preferencial': fila_preferencial,
                'fila_normal': fila_normal
            }

            return render(request, 'detalhes_autorizacao.html', {'context': context})
        else:
            context = {
                'autorizacao': autorizacao,
                'msg_error': 'Autorização sem fila'
            }
            return render(request, 'detalhes_autorizacao.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def encerrarAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        fila_normal = None
        fila_preferencial = None

        if request.method == 'POST':
            autorizacao.status = 'ENCERRADA'
            autorizacao.save()
            
            for fila in autorizacao.filas.all():
                if fila.fila_preferencial:
                    fila_preferencial = fila
                    fila_preferencial.status = "ENCERRADA"
                    fila_preferencial.save()
                else:
                    fila_normal = fila
                    fila_normal.status = "ENCERRADA"
                    fila_normal.save()

            context = {
                'autorizacao': autorizacao,
                'fila_preferencial': fila_preferencial,
                'fila_normal': fila_normal
            }

            return render(request, 'detalhes_autorizacao.html', {'context': context})
        
        return render(request, 'encerrar_autorizacao.html', {'autorizacao': autorizacao})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def detalhesAutorizacaoUsuario(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        unidade = UnidadeSaude.objects.filter(autorizacoes=autorizacao)

        context = {
            'autorizacao': autorizacao,
            'unidade': unidade[0]
        }

        return render(request, 'detalhes_autorizacao_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaAutorizacoesAguardando(request):
    if has_permission(request.user, 'permissao_unidade'):
        hoje = date.today()
        unidade = UnidadeSaude.objects.filter(users=request.user)
        autorizacoes = unidade[0].autorizacoes.filter(status='AGUARDANDO', data=hoje)

        if autorizacoes:
            context = {
                'autorizacoes': autorizacoes
            }
        else:
            context = {
                'msg_error': 'Nenhuma autorizacao aguardando para a data de hoje!'
            }

        return render(request, 'lista_autorizacoes_aguardando.html', {'context': context})
    
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioListaAutorizacao(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_lista_autorizacao.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_lista_autorizacao.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_lista_autorizacao.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_lista_autorizacao.pdf'
        return response
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioAutorizacao(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_autorizacao.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_autorizacao.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_autorizacao.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_autorizacao.pdf'
        return response
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

class Context(object):
    def __init__(self, context):
        self.__context = context
    
    def get(self):
        return self.__context

    def set(self, context):
        self.__context = context

contexto = Context(None)




