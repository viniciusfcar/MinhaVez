from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fila
from consulta.models import Consulta
from usuario.models import Usuario
from exame.models import Exame
from .forms import FormFila
from autorizacao.models import Autorizacao
from unidadeSaude.models import UnidadeSaude
from rest_framework import viewsets
from .serializers import FilaSerializer
from agendamento.models import Agendamento
from ficha.models import Ficha
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from notificacoes import views as notificacoes
from datetime import date, datetime


class GetFilaViewSet(viewsets.ModelViewSet):
    serializer_class = FilaSerializer

    def get_queryset(self):
        queryset = Fila.objects.all()
        return queryset

    @action(methods=['get'], detail=True)
    def fila_ficha(self, request, pk=None):
        ficha = get_object_or_404(Ficha, pk=pk)
        filas = Fila.objects.filter(fichas=ficha)
        tmpJson = serializers.serialize("json", filas)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


@login_required(login_url='/accounts/login')
def cadastroFilaConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        form = FormFila(request.POST or None, request.FILES or None)

        if consulta.user == request.user:
            if form.is_valid():
                total_fichas = form.cleaned_data['vagas']
                vagas = total_fichas
                
                if consulta.agendamento:
                    total_usuarios = consulta.agendamento.usuarios.count()
                    vagas -= total_usuarios

                fila_normal = Fila(nome=form.cleaned_data['nome'], vagas=vagas, total_fichas=total_fichas, status='INICIADA')
                fila_normal.fila_preferencial = False
                fila_preferencial = Fila(nome=form.cleaned_data['nome']+' PREFERENCIAL', vagas=vagas, total_fichas=total_fichas, status='INICIADA')
                fila_preferencial.fila_preferencial = True
                fila_normal.save()
                fila_preferencial.save()
                consulta.filas.add(fila_normal)
                consulta.filas.add(fila_preferencial)
                consulta.create_fila = True
                
                if consulta.verifica:
                    consulta.agendamento.participar = True
                    consulta.agendamento.save()
                
                consulta.save()
                
                if consulta.agendamento:
                    if consulta.agendamento.usuarios.all():
                        #NOTIFICAÇÂO
                        mensagem = 'Atenção, a consulta: '+ consulta.nome + ' iniciou suas filas, marque seu lugar na fila desejada!'
                        notificacoes.notificacaoAgendamento(request, mensagem, consulta.agendamento)

                return redirect('detalhesConsulta', id=consulta.id)
        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }

            return render(request, 'home_usuario.html', {'context': context})

        return render(request, 'cadastro_fila_consulta.html', {'form': form})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def cadastroFilaAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        form = FormFila(request.POST or None, request.FILES or None)

        if autorizacao.user == request.user:
            if form.is_valid():
                
                total_fichas = form.cleaned_data['vagas']
                vagas = total_fichas

                if autorizacao.agendamento:
                    total_usuarios = autorizacao.agendamento.usuarios.count()
                    vagas -= total_usuarios

                fila = Fila(nome=form.cleaned_data['nome'], vagas=vagas, total_fichas=total_fichas)
                fila.fila_preferencial = False
                preferencial = Fila(nome=form.cleaned_data['nome']+' PREFERENCIAL', vagas=vagas, total_fichas=total_fichas)
                preferencial.fila_preferencial = True
                fila.save()
                preferencial.save()
                autorizacao.filas.add(fila)
                autorizacao.filas.add(preferencial)
                autorizacao.create_fila = True

                #Faz com que o úsuario possa participar da fila pelo agendamento
                if autorizacao.verifica:
                    autorizacao.agendamento.participar = True
                    autorizacao.agendamento.save()
                autorizacao.save()

                if autorizacao.agendamento:
                    if autorizacao.agendamento.usuarios.all():
                        #NOTIFICAÇÂO
                        mensagem = 'Atenção, a autorização: '+ autorizacao.nome + ' iniciou suas filas, marque seu lugar na fila desejada!'
                        notificacoes.notificacaoAgendamento(request, mensagem, autorizacao.agendamento)

                return redirect('detalhesAutorizacao', id=autorizacao.id)
        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }

            return render(request, 'home_unidade_saude.html', {'context': context})

        return render(request, 'cadastro_fila_autorizacao.html', {'form': form})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def cadastroFilaExame(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        exame = get_object_or_404(Exame, pk=id)
        form = FormFila(request.POST or None, request.FILES or None)

        if exame.user == request.user:
            if form.is_valid():

                total_fichas = form.cleaned_data['vagas']
                vagas = total_fichas

                if exame.agendamento:
                    total_usuarios = consulta.agendamento.usuarios.count()
                    vagas -= total_usuarios

                fila = Fila(nome=form.cleaned_data['nome'], vagas=vagas, total_fichas=total_fichas)
                fila.fila_preferencial = False
                preferencial = Fila(nome=form.cleaned_data['nome']+' PREFERENCIAL', vagas=vagas, total_fichas=total_fichas)
                preferencial.fila_preferencial = True
                fila.save()
                preferencial.save()
                exame.filas.add(fila)
                exame.filas.add(preferencial)
                exame.create_fila = True
                if exame.verifica:
                    exame.agendamento.participar = True
                    exame.agendamento.save()
                exame.save()

                if exame.agendamento:
                    if exame.agendamento.usuarios.all():
                        #NOTIFICAÇÂO
                        mensagem = 'Atenção, o exame: '+ exame.nome + ' iniciou suas filas, marque seu lugar na fila desejada!'
                        notificacoes.notificacaoAgendamento(request, mensagem, exame.agendamento)

                return redirect('detalhesExame', id=exame.id)
        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }

            return render(request, 'home.html', {'context': context})

        return render(request, 'cadastro_fila_exame.html', {'form': form})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaFila(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        filas = [None]
        aux_filas = [None]
        hoje = date.today()
        consultas = None
        autorizacoes = None
        exames = None
        objetos_aux = None

        if unidade:

            if request.method == 'POST':
                data = request.POST.get('data', None)
                dataFinal = request.POST.get('dataFinal', None)
                objeto = request.POST.get('objeto', None)
                
                if objeto == 'Consultas':
                    obj_aux = 'Consultas'
                    consultas = unidade[0].consultas.all()
                    objetos = unidade[0].consultas.filter(data=hoje, create_fila=True).order_by('hora', 'data')
                elif objeto == 'Autorizacoes':
                    obj_aux = 'Autorizacoes'
                    autorizacoes = unidade[0].autorizacoes.all()
                    objetos = unidade[0].autorizacoes.filter(data=hoje, create_fila=True).order_by('hora', 'data')
                elif objeto == 'Exames':
                    obj_aux = 'Exames'
                    exames = unidade[0].exames.all()
                    objetos = unidade[0].exames.filter(data=hoje, create_fila=True).order_by('hora', 'data')

                context = {
                    'objeto': obj_aux
                }

                if objetos:
                    context['objetos'] = objetos

                else:
                    context['msg_alert'] = 'Não possui Filas para hoje'

                if data:
                    try:
                        if consultas:
                            objetos_aux = unidade[0].consultas.filter(data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')], create_fila=True).order_by('hora', 'data')
                        elif autorizacoes:
                            objetos_aux = unidade[0].autorizacoes.filter(data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')], create_fila=True).order_by('hora', 'data')
                        elif exames:
                            objetos_aux = unidade[0].exames.filter(data__range=[datetime.strptime(data, '%Y-%m-%d'), datetime.strptime(dataFinal, '%Y-%m-%d')], create_fila=True).order_by('hora', 'data')
                        
                        if objetos_aux:
                            context['objetos'] = objetos_aux
                            context['msg_alert'] = None
                        
                        else:
                            context['msg_busca'] = 'Nada encontrado para esses parâmetros!'
                    
                    except ValueError:
                        context['msg_busca'] = 'Informe uma data válida!'

                return render(request, 'lista_fila.html', {'context': context})
            
            return render(request, 'lista_fila.html')

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
def deleteFila(request, id_fila, id_fila_pref):
    if has_permission(request.user, 'permissao_unidade'):
        fila = get_object_or_404(Fila, pk=id_fila)
        fila_pref = get_object_or_404(Fila, pk=id_fila_pref)

        consulta = Consulta.objects.filter(filas=fila)
        autorizacao = Autorizacao.objects.filter(filas=fila)
        exame = Exame.objects.filter(filas=fila)

        if request.method == 'POST':
            if consulta:
                if consulta[0].user == request.user:
                    fila.fichas.all().delete()
                    fila_pref.fichas.all().delete()
                    fila.delete()
                    fila_pref.delete()
                    consulta[0].create_fila = False
                    consulta[0].save()
                    return redirect('detalhesConsulta', id=consulta[0].id)
                
            elif autorizacao:
                if autorizacao[0].user == request.user:
                    fila.delete()
                    fila_pref.delete()
                    autorizacao[0].create_fila = False
                    autorizacao[0].save()
                    return redirect('detalhesAutorizacao', id=autorizacao[0].id)

            elif exame:
                if exame[0].user == request.user:
                    fila.delete()
                    fila_pref.delete()
                    exame[0].create_fila = False
                    exame[0].save()
                    return redirect('detalhesExame', id=exame[0].id)

        return render(request, 'delete_fila.html', {'fila': fila})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})    


@login_required(login_url='/accounts/login')
def detalhesFila(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        fila = get_object_or_404(Fila, pk=id)
        consulta = Consulta.objects.filter(filas=fila)
        autorizacao = Autorizacao.objects.filter(filas=fila)
        exame = Exame.objects.filter(filas=fila)
        fichas = fila.fichas.all().order_by('numero')
        data = date.today()

        if consulta is None and autorizacao is None:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }

            return render(request, 'home.html', {'context': context})
        
        elif exame is None:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'
            }

            return render(request, 'home.html', {'context': context})
        
        elif consulta:
            if fichas:
                context = {
                    'consulta': consulta[0],
                    'fila': fila,
                    'fichas': fichas,
                    'data': data
                }

            else:
                context = {
                    'consulta': consulta[0],
                    'fila': fila,
                    'data': data
                }

        elif autorizacao:
            if fichas:
                context = {
                    'autorizacao': autorizacao[0],
                    'fila': fila,
                    'fichas': fichas,
                    'data': data
                }

            else:
                context = {
                    'autorizacao': autorizacao[0],
                    'fila': fila,
                    'data': data
                }
        elif exame:
            if fichas:
                context = {
                    'exame': exame[0],
                    'fila': fila,
                    'fichas': fichas,
                    'data': data
                }

            else:
                context = {
                    'exame': exame[0],
                    'fila': fila,
                    'data': data
                }

        contexto.set(context)
        
        return render(request, 'detalhes_fila.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def adicionarUsuarioFila(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        
        fila = get_object_or_404(Fila, pk=id)
        consulta = Consulta.objects.filter(filas=fila)
        autorizacao = Autorizacao.objects.filter(filas=fila)
        exame = Exame.objects.filter(filas=fila)
        contem = False
        usuario_cpf = None
        usuario_sus = None
        fila_normal = None
        fila_preferencial = None

        #ESTE VETOR SERVE PARA PEGAR AS DUAS FILAS
        #E DIFERENCIAR A NORMAL DA PREFERENCIAL
        vetor = []

        if consulta:
            vetor = consulta[0].filas.all()
            fila_normal = vetor[0]
            fila_preferencial = vetor[1]

            context = {
                'fila': fila,
                'consulta': consulta[0],
                'fichas': fila.fichas.all(),
            }

        if autorizacao:
            vetor = autorizacao[0].filas.all()
            fila_normal = vetor[0]
            fila_preferencial = vetor[1]

            context = {
                'fila': fila,
                'autorizacao': autorizacao[0],
                'fichas': fila.fichas.all(),
            }

        if exame:
            vetor = exame[0].filas.all()
            fila_normal = vetor[0]
            fila_preferencial = vetor[1]

            context = {
                'fila': fila,
                'exame': exame[0],
                'fichas': fila.fichas.all(),
            }

        if request.method == 'POST':
            cpf = request.POST.get('cpf', None)
            sus = request.POST.get('sus', None)

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

            contem_normal = fila_normal.fichas.filter(usuario=usuario).exists()
            contem_preferencial = fila_preferencial.fichas.filter(usuario=usuario).exists()

            if contem_normal or contem_preferencial:
                context = {
                    'fila': fila,
                    'msg_alert': 'Cidadão já está nesta fila ou na outra!'
                }

                return render(request, 'adicionar_usuario_fila.html', {'context': context})
            
            else:
                if usuario:
                    if fila:
                        num_ficha = 1
                        for ficha in fila.fichas.all():
                            if num_ficha == fila.total_fichas:
                                fila_normal.total_fichas += 1
                                fila_preferencial.total_fichas += 1
                                num_ficha += 1
                            num_ficha += 1

                        ficha = Ficha(numero=num_ficha, usuario= usuario, preferencial=True, status='AGUARDANDO', excluida=False)
                        ficha.save()
                        fila.fichas.add(ficha)
                        
                        if fila.vagas > 0:
                            fila_normal.vagas -= 1
                            fila_preferencial.vagas -= 1

                        fila.save()
                        fila_normal.save()
                        fila_preferencial.save()
                        
                        if fila.fila_preferencial:
                            context['fila'] = fila_preferencial
                        else:
                            context['fila'] = fila_normal
                        
                        return render(request, 'detalhes_fila.html', {'context': context})
                else:
                    context = {
                        'fila': fila,
                        'msg_alert': 'Cidadão não localizado, informe um número correto.'
                    }

                    return render(request, 'adicionar_usuario_fila.html', {'context': context})
                
        return render(request, 'adicionar_usuario_fila.html', {'context': context})
    
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def naoCompareceu(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        ficha = get_object_or_404(Ficha, pk=id)
        fila = Fila.objects.filter(fichas=ficha)
        consulta = Consulta.objects.filter(filas=fila[0])
        autorizacao = Autorizacao.objects.filter(filas=fila[0])
        exame = Exame.objects.filter(filas=fila[0])
        
        context = {
            'ficha': ficha,
            'fila': fila[0],
        }

        if request.method == 'POST':
            ficha.status = 'NÃO COMPARECEU'
            ficha.save()

            if consulta:
                if fila[0].fichas.all():
                    context = {
                        'consulta': consulta[0],
                        'fila': fila[0],
                        'fichas': fila[0].fichas.all()
                    }

                else:
                    context = {
                        'consulta': consulta[0],
                        'fila': fila[0]
                    }

            elif autorizacao:
                if fila[0].fichas.all():
                    context = {
                        'autorizacao': autorizacao[0],
                        'fila': fila[0],
                        'fichas': fila[0].fichas.all()
                    }

                else:
                    context = {
                        'autorizacao': autorizacao[0],
                        'fila': fila[0]
                    }
            elif exame:
                if fila[0].fichas.all():
                    context = {
                        'exame': exame[0],
                        'fila': fila[0],
                        'fichas': fila[0].fichas.all()
                    }

                else:
                    context = {
                        'autorizacao': autorizacao[0],
                        'fila': fila[0]
                    }
            return render(request, 'detalhes_fila.html', {'context': context})
        
        return render(request, 'nao_compareceu.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioFila(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_fila.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_fila.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_fila.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_fila.pdf'
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


