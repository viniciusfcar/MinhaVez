from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Especialista
from usuario.models import Usuario
from .forms import FormEspecialista
from unidadeSaude.models import UnidadeSaude
from rest_framework.viewsets import ModelViewSet
from .serializers import EspecialistaSerializer
from especializacao.models import Especializacao
from profissao.models import Profissao
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from weasyprint import HTML
from rolepermissions.checkers import has_permission
from unidadeSaude.serializers import UnidadeSaudeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework.filters import SearchFilter
from rest_framework import status
from datetime import date


class GetEspecialistaViewSet(ModelViewSet):
    serializer_class = EspecialistaSerializer    
    filter_backends = (SearchFilter,)
    search_fields = ['^nome', '^sobrenome', '^especializacao__nome', '^profissao__nome']

    def get_queryset(self):
        queryset = Especialista.objects.all()
        return queryset

    @action(methods=['get'], detail=True)
    def unidadesEspecialista(self, request, pk=None):
        especialista = get_object_or_404(Especialista, pk=pk)
        unidades = UnidadeSaude.objects.filter(especialistas=especialista)
        tmpJson = serializers.serialize("json", unidades)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))
    
    @action(methods=['get'], detail=False)
    def consultaEspecialista(self, request):
        especialista = Especialista.objects.filter(num_conselho=request.GET.get('num_conselho'), conselho=request.GET.get('conselho'), estado_conselho=request.GET.get('estado_conselho'))
        
        if especialista:
            tmpJson = serializers.serialize("json", especialista)
            tmpObj = json.loads(tmpJson)
            return HttpResponse(json.dumps(tmpObj))
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

@login_required(login_url='/accounts/login')
def cadastroEspecialista(request):
    if has_permission(request.user, 'permissao_unidade'):
        form = FormEspecialista(request.POST or None, request.FILES or None)

        if form.is_valid():
            especialista = Especialista.objects.filter(num_conselho=request.POST.get('num_conselho'), conselho=request.POST.get('conselho'))
            
            if especialista:
                context = {
                    'form': form,
                    'msg_error': 'Especialista já cadastrado com os parâmteros:',
                }
                return render(request, 'cadastro_especialista.html', {'context': context})
            else:
                especialista = Especialista(nome=request.POST.get('nome'), sobrenome=request.POST.get('sobrenome'),
                                            profissao=form.cleaned_data['profissao'],
                                            num_conselho=request.POST.get('num_conselho'),
                                            conselho=request.POST.get('conselho'), estado_conselho=request.POST.get('estado_conselho'),
                                            imagem=request.FILES['imagem'])
                                            
                especialista.save()
                especializacoes = request.POST.getlist('especializacao[]')
                
                especialista.especializacao.set(especializacoes)
                
                especialista.save()

                unidade = UnidadeSaude.objects.filter(users=request.user)
                if unidade:
                    unidade[0].especialistas.add(especialista)
                    unidade[0].save()

                return redirect('listaEspecialista')

        context = {
            'form': form,
            'especializacoes': Especializacao.objects.all(),
        }

        return render(request, 'cadastro_especialista.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def vinculaEspecialistaUnidade(request):
    if has_permission(request.user, 'permissao_unidade'):
        form = FormEspecialista(request.POST or None, request.FILES or None)
        
        if request.method == 'POST':
            id = request.POST.get('id_especialista')
            especialista = get_object_or_404(Especialista, pk=id)
            unidade = UnidadeSaude.objects.filter(users=request.user)
            
            unidade[0].especialistas.add(especialista)
            unidade[0].save()

            return redirect('listaEspecialista')
        
        context = {
            'form': form
        }
        return render(request, 'cadastro_especialista.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaEspecialista(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        pesquisa = request.GET.get('pesquisa', None)
        data = date.today()

        if unidade:
            especialistas = unidade[0].especialistas.all()
            
            if pesquisa:
                profissao = Profissao.objects.filter(nome__contains=pesquisa)
                especializacao = Especializacao.objects.filter(nome__contains=pesquisa)
                
                if profissao:
                    
                    especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa) | especialistas.filter(profissao__nome__icontains=profissao[0])
                    
                    if especialistas:
                        context = {
                            'especialistas': especialistas,
                            'data': data
                        }
                    else:
                        especialistas = unidade[0].especialistas.all()
                        context = {
                            'especialistas': especialistas,
                            'msg_busca': 'Nada encontrado para esses parâmetros!',
                            'data': data
                        }

                elif especializacao:
                    especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa) | especialistas.filter(especializacao__nome__icontains=especializacao[0])
                    if especialistas:
                        context = {
                            'especialistas': especialistas,
                            'data': data
                        }
                    else:
                        especialistas = unidade[0].especialistas.all()
                        context = {
                            'especialistas': especialistas,
                            'msg_busca': 'Nada encontrado para esses parâmetros!',
                            'data': data
                        }
                elif pesquisa:
                    especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa)
                    if especialistas:
                        context = {
                            'especialistas': especialistas,
                            'data': data
                        }
                    else:
                        especialistas = unidade[0].especialistas.all()
                        context = {
                            'especialistas': especialistas,
                            'msg_busca': 'Nada encontrado para esses parâmetros!',
                            'data': data
                        }
                else:
                    especialistas = unidade[0].especialistas.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!',
                        'data': data
                    }

            elif especialistas:
                context = {
                    'especialistas': especialistas,
                    'data': data
                }

            else:
                context = {
                    'msg_alert': 'Ainda não possuem Especialistas cadastrados!',
                    'data': data
                }
            
            contexto.set(context)

            return render(request, 'lista_especialista.html', {'context': context})

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
def alterarEspecialista(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        especialista = get_object_or_404(Especialista, pk=id)

        form = FormEspecialista(request.POST or None, request.FILES or None, instance=especialista)

        if form.is_valid():
            especialista.num_conselho=request.POST.get('num_conselho')
            especialista.conselho=request.POST.get('conselho')
            especialista.estado_conselho=request.POST.get('estado_conselho')
            especializacoes = request.POST.getlist('especializacao[]')

            especialista.especializacao.set(especializacoes)

            form.save()
            especialista.save()
            
            return redirect('listaEspecialista')
        
        context = {
            'form': form,
            'especialista': especialista,
            'especializacoes': Especializacao.objects.all(),
        }

        return render(request, 'cadastro_especialista.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def deleteEspecialista(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        especialista = get_object_or_404(Especialista, pk=id)
        unidade = UnidadeSaude.objects.filter(users=request.user)

        if request.method == 'POST':
            unidade[0].especialistas.remove(especialista)
            unidade[0].save()
            return redirect('listaEspecialista')

        return render(request, 'delete_especialista.html', {'nome': especialista.nome})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaEspecilistaUsuario(request):
    if has_permission(request.user, 'permissao_usuario'):
        especialistas = Especialista.objects.all()
        pesquisa = request.GET.get('pesquisa', None)
        user = request.user
        usuario = Usuario.objects.get(user=user)

        if pesquisa:
            profissao = Profissao.objects.filter(nome__icontains=pesquisa)
            especializacao = Especializacao.objects.filter(nome__icontains=pesquisa)
            
            if profissao:
                especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa) | especialistas.filter(profissao__nome__icontains=profissao[0])
                if especialistas:
                    context = {
                        'especialistas': especialistas,
                    }
                else:
                    especialistas = especialistas = Especialista.objects.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }

            elif especializacao:
                especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa) | especialistas.filter(__nome__icontains=especializacao[0])
                if especialistas:
                    context = {
                        'especialistas': especialistas,
                    }
                else:
                    especialistas = especialistas = Especialista.objects.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }
            elif pesquisa:
                especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa)
                
                if especialistas:
                    context = {
                        'especialistas': especialistas,
                    }
                else:
                    especialistas = Especialista.objects.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }
        elif especialistas:
            context = {
                'especialistas': especialistas,
            }
        else:
            context = {
                'msg_error': 'Nenhum especialista cadastrado!'
            }
        
        return render(request, 'lista_especialista_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def detalhesEspecialistaUsuario(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        especialista = get_object_or_404(Especialista, pk=id)
        unidades = UnidadeSaude.objects.filter(especialistas=especialista)

        if unidades is None:
            context = {
                'especialista': especialista,
            }
        else:
            context = {
                'unidades': unidades,
                'especialista': especialista,
            }
        return render(request, 'detalhes_especialista_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


def relatorioEspecialista(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_especialista.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_especialista.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_especialista.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_especialista.pdf'
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

