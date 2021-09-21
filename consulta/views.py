from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Consulta
from .forms import FormConsulta
from usuario.models import Usuario
from django.contrib.auth.models import User
from ficha.models import Ficha
from fila.models import Fila
from unidadeSaude.models import UnidadeSaude
from rest_framework import viewsets
from .serializers import ConsultaSerializer
from datetime import date, datetime
from autorizacao.models import Autorizacao
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from especialista.models import Especialista
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework.filters import SearchFilter
from notificacoes import views as notificacoes
from rest_framework import status

class GetConsultaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultaSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^nome', '^data', '^status', '^especialista__nome', '^especialista__profissao__nome', '^especialista__especializacao__nome')

    def get_queryset(self):
        queryset = Consulta.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
        return queryset

    @action(methods=['get'], detail=True)
    def consulta_ficha(self, request, pk=None):
        ficha = get_object_or_404(Ficha, pk=pk)
        filas = Fila.objects.filter(fichas=ficha)
        consulta = Consulta.objects.filter(filas=filas[0])
        tmpJson = serializers.serialize("json", consulta)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

    @action(methods=['get'], detail=True)
    def get_status_consulta(self, request, pk=None):
        consulta = get_object_or_404(Consulta, pk=pk)

        if consulta.status == 'INICIADA':
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@login_required(login_url='/accounts/login')
def cadastroConsulta(request):
    if has_permission(request.user, 'permissao_unidade'):
        
        if request.method == 'POST':

            try:
                datetime.strptime(request.POST.get('hora'), '%H:%M')
                datetime.strptime(request.POST.get('data'), '%Y-%m-%d')

                esp = Especialista.objects.get(id=request.POST.get('especialista'))
                consulta = Consulta(nome=request.POST.get('nome'), data=request.POST.get('data'), hora=request.POST.get('hora'))
                
                consulta.especialista = esp
                consulta.user = request.user
                consulta.create_fila = False
                consulta.status = "AGUARDANDO"
                
                consulta.save()
                unidade = UnidadeSaude.objects.filter(users=request.user)

                if unidade:
                    unidade[0].consultas.add(consulta)
                    unidade[0].save()

                return redirect('listaConsulta')
            
            except ValueError:
                unidade = UnidadeSaude.objects.filter(users=request.user)
                context = {
                    'especialistas': unidade[0].especialistas.all
                }

                return render(request, 'cadastro_consulta.html', {'context': context})

        else:
            unidade = UnidadeSaude.objects.filter(users=request.user)
            context = {
                'especialistas': unidade[0].especialistas.all
            }

        return render(request, 'cadastro_consulta.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaConsulta(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        pesquisa = request.GET.get('pesquisa', None)
        data = request.GET.get('data', None)
        dataFinal = request.GET.get('dataFinal', None)
        data_rel = date.today()

        if unidade:
            consultas = unidade[0].consultas.all().extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-create_fila', '-status')

            context = {
                'data': data_rel
            }

            if consultas:
                context['consultas'] = consultas
            
            if pesquisa:
                espe = Especialista.objects.filter(nome__icontains=pesquisa)

                if espe:
                    consultas_aux = unidade[0].consultas.filter(nome__icontains=pesquisa) | consultas.filter(status__icontains=pesquisa) | consultas.filter(especialista=espe[0])

                    if consultas_aux:
                        context['consultas'] = consultas_aux
                    
                    else:
                        context['msg_busca'] = 'Nada encontrado para esses parâmetros!'
                
                else:
                    consultas_aux = unidade[0].consultas.filter(nome__icontains=pesquisa) | consultas.filter(status__icontains=pesquisa)
                    
                    if consultas_aux:
                        context['consultas'] = consultas_aux

                    else:
                        context['msg_busca'] = 'Nada encontrado para esses parâmetros!'

            if data:
                try:
                    consultas_aux = unidade[0].consultas.filter(data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')]).order_by('data', 'hora', '-create_fila', '-status')
                    
                    if consultas_aux:
                        context['consultas'] = consultas_aux
                    
                    else:
                        context['msg_busca'] = 'Nada encontrado para esses parâmetros!'

                except ValueError:
                    context['msg_busca'] = 'Informe uma data válida!'
            
            if not consultas:
                consultas_aux = unidade[0].consultas.all()
                
                if consultas_aux:
                    context['msg_alert'] = 'Nenhuma Consulta em aguardo!'
                
                else:
                    context['msg_alert'] = 'Nenhuma Consulta cadastrada!'

            contexto.set(context)
            
            return render(request, 'lista_consulta.html', {'context': context})

        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'

            }

        return render(request, 'home_unidade_saude.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def alterarConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        consulta = get_object_or_404(Consulta, pk=id)
        fila_normal = None
        fila_preferencial = None

        
        if consulta.filas.all():
            for fila in consulta.filas.all():
                if fila.fila_preferencial:
                    fila_preferencial = fila
                else:
                    fila_normal = fila

        if request.method == 'POST':
            if consulta.user == request.user: 
                try:
                    datetime.strptime(request.POST.get('hora'), '%H:%M')
                    datetime.strptime(request.POST.get('data'), '%Y-%m-%d')

                    esp = Especialista.objects.get(id=request.POST.get('especialista'))

                    consulta.nome = request.POST.get('nome')
                    consulta.hora = request.POST.get('hora')
                    consulta.data = request.POST.get('data')
                    consulta.especialista = esp

                    consulta.save()

                    #NOTIFICAÇÂO
                    mensagem = 'Atenção, a consulta: '+ consulta.nome + 'teve uma alteração, fique atento!'

                    if fila_normal:
                        if fila_normal.fichas.all():
                            notificacoes.notificacaoColetiva(request, mensagem, fila_normal.fichas.all())
                    
                    if fila_preferencial:
                        if fila_preferencial.fichas.all():
                            notificacoes.notificacaoColetiva(request, mensagem, fila_preferencial.fichas.all())
                    
                    if consulta.agendamento:
                        if consulta.agendamento.usuarios.all():
                            notificacoes.notificacaoAgendamento(request, mensagem, consulta.agendamento)
                    
                    return redirect('listaConsulta')
                
                except ValueError:
                    context = {
                        'consulta': consulta,
                    }

                    return render(request, 'cadastro_consulta.html', {'context': context})
            else:
                context = {
                    'msg_error': 'Indisponivel Acessar Essa Área'

                }
                return redirect('homeUnidadeSaude', {'context': context})
        
        
        context = {
            'consulta': consulta,
            'especialistas': unidade[0].especialistas.all
        }

        return render(request, 'cadastro_consulta.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def deleteConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        fila_normal = None
        fila_preferencial = None
        agendamento = consulta.agendamento

        for fila in consulta.filas.all():
            if fila.fila_preferencial:
                fila_preferencial = fila
            else:
                fila_normal = fila

        if consulta.user == request.user:
            if request.method == 'POST':
                if fila_normal != None:
                    fila_normal.delete()
                    fila_preferencial.delete()
                
                if agendamento != None:
                    agendamento.delete()
                    
                consulta.delete()
                return redirect('listaConsulta')
        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'

            }
            return redirect('homeUnidadeSaude', {'context': context})

        return render(request, 'delete_consulta.html', {'nome': consulta.nome})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def detalhesConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        fila_normal = None
        fila_preferencial = None
        fichas_normais = [None]
        fichas_preferenciais = [None]
        data = date.today()

        for fila in consulta.filas.all():
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
            'consulta': consulta,
            'fila_preferencial': fila_preferencial,
            'fila_normal': fila_normal,
            'fichas_normais': fichas_normais,
            'fichas_preferenciais': fichas_preferenciais,
            'data': date.today
        }

        contexto.set(context)
        return render(request, 'detalhes_consulta.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

#METODOS QUE POSSIVELMENTE NÃO ESTOU MAIS USANDO
'''
@login_required(login_url='/accounts/login')
def adicionaUsuarioConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        usuario = Usuario.objects.filter(user=request.user)

        if consulta.vagas > 0:
            consulta.usuarios.append(usuario)
        if consulta.user == request.user:
            if usuario:
                consulta.usuarios.add(usuario[0])
                context = {
                    'consulta': consulta,
                    'usuarios': consulta.usuarios
                }
            else:
                usuarios = consulta.usuarios
                context = {
                    'consulta': consulta,
                    'usuarios': usuarios
                }
                print('CPF não localizado')
        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'

            }
            return redirect('homeUnidadeSaude', {'context': context})

        return render(request, 'detalhes_consulta.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def excluiUsuarioConsulta(request, cpf, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        usuario = Usuario.objects.filter(cpf=cpf)

        if consulta.user == request.user:
            context = {
                'consulta': consulta,
                'usuarios': consulta.usuarios,
                'usuario': usuario[0],
            }

            if request.method == 'POST':
                consulta.usuarios.remove(usuario[0])
                return redirect('detalhesAtendimento', id=consulta.id)

        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'

            }
            return redirect('homeUnidadeSaude', {'context': context})

        return render(request, 'exclui_usuario_consulta.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})
'''

@login_required(login_url='/accounts/login')
def listaConsultaUsuario(request):
    if has_permission(request.user, 'permissao_usuario'):
        consultas = Consulta.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
        pesquisa = request.GET.get('pesquisa', None)
        espe = Especialista.objects.filter(nome=request.GET.get('pesquisa', None))
        data = request.GET.get('data', None)

        if espe:
            consultas = consultas.filter(especialista__icontains=espe[0]) | consultas.filter(nome__icontains=pesquisa) | consultas.filter(status__icontains=pesquisa)

            if consultas:
                context = {
                    'consultas': consultas,
                }
            else:
                consultas = Consulta.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
                context = {
                    'consultas': consultas,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif data:
            try:
                datetime.strptime(data, '%Y-%m-%d')
                consultas = consultas.filter(data=data).order_by('hora', 'data', '-create_fila', '-status')

                if consultas:
                    context = {
                        'consultas': consultas,
                    }
                else:
                    consultas = Consulta.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
                    context = {
                        'consultas': consultas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }

            except ValueError:
                consultas = Consulta.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
                context = {
                    'consultas': consultas,
                    'msg_busca': 'Informe uma data válida!'
                }

        elif pesquisa:
            consultas = consultas.filter(nome__icontains=pesquisa) | consultas.filter(status__icontains=pesquisa)

            if consultas:
                context = {
                    'consultas': consultas,
                }
            else:
                consultas = Consulta.objects.extra(where=['status <> "ENCERRADA"']).order_by('data', 'hora', '-status')
                context = {
                    'consultas': consultas,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif consultas:
            context = {
                'consultas': consultas
            }
        else:
            context = {
                'msg_error': 'Nenhuma consulta cadastrada!'
            }
        
        return render(request, 'lista_consulta_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def detalhesConsultaUsuario(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        consulta = get_object_or_404(Consulta, pk=id)
        unidade = UnidadeSaude.objects.filter(consultas=consulta)

        context = {
            'consulta': consulta,
            'unidade': unidade[0]
        }

        return render(request, 'detalhes_consulta_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def iniciarConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        fila_normal = None
        fila_preferencial = None

        if consulta.filas.all():
            for fila in consulta.filas.all():
                if fila.fila_preferencial:
                    fila_preferencial = fila
                else:
                    fila_normal = fila

            consulta.status = "INICIADA"
            consulta.save()
            
            if consulta.filas.all():
                if fila_normal.fichas.all() or fila_preferencial.fichas.all():
                    #PARTE DO ENVIO DA NOTIFICACAO
                    mensagem = "A consulta: " + consulta.nome + " foi iniciada, fique atento para não perder a sua vez!"
                    notificacoes.inicioConsultaAutorizacao(request, mensagem, consulta)

            context = {
                'consulta': consulta,
                'fila_preferencial': fila_preferencial,
                'fila_normal': fila_normal
            }

            return render(request, 'detalhes_consulta.html', {'context': context})
        else:
            context = {
                'consulta': consulta,
                'msg_error': 'Consulta sem fila!'
            }
            return render(request, 'detalhes_consulta.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def encerrarConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        fila_normal = None
        fila_preferencial = None

        if request.method == 'POST':
            for fila in consulta.filas.all():
                if fila.fila_preferencial:
                    fila_preferencial = fila
                    fila_preferencial.status = "ENCERRADA"
                    fila_preferencial.save()
                else:
                    fila_normal = fila
                    fila_normal.status = "ENCERRADA"
                    fila_normal.save()
            
            consulta.status = "ENCERRADA"
            consulta.save()
            
            context = {
                'consulta': consulta,
                'fila_preferencial': fila_preferencial,
                'fila_normal': fila_normal
            }

            return render(request, 'detalhes_consulta.html', {'context': context})
        
        return render(request, 'encerrar_consulta.html', {'consulta': consulta})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaConsultasAguardando(request):
    if has_permission(request.user, 'permissao_unidade'):
        hoje = date.today()
        unidade = UnidadeSaude.objects.filter(users=request.user)
        consultas = unidade[0].consultas.filter(status='AGUARDANDO', data=hoje)

        if consultas:
            context = {
                'consultas': consultas
            }
        else:
            context = {
                'msg_error': 'Nenhuma consulta aguardando para a data de hoje!'
            }
        
        return render(request, 'lista_consultas_aguardando.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context}) 

@login_required(login_url='/accounts/login')
def relatorioListaConsulta(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_lista_consulta.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_lista_consulta.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_lista_consulta.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_lista_consulta.pdf'
        return response
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioConsulta(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_consulta.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_consulta.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_consulta.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_consulta.pdf'
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

    
    
    