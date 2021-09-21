from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UnidadeSaude
from ficha.models import Ficha
from fila.models import Fila
from consulta.models import Consulta
from autorizacao.models import Autorizacao
from especialista.models import Especialista
from responsavel.models import Responsavel
from profissao.models import Profissao
from especializacao.models import Especializacao
from exame.models import Exame
from .forms import FormUnidadeSaude, FormUser
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .serializers import UnidadeSaudeSerializer
from rolepermissions.checkers import has_permission
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.core import serializers
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from django.core.validators import validate_email


class GetUnidadeSaudeViewSet(viewsets.ModelViewSet):
    serializer_class = UnidadeSaudeSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^razao_social','^logradouro', '^bairro', '^cidade', '^estado', '^especialistas__nome', '^responsaveis__nome')

    def get_queryset(self):
        queryset =  UnidadeSaude.objects.all()
        return queryset
    
    @action(methods=['get'], detail=True)
    def unidade_ficha(self, request, pk=None):
        ficha = get_object_or_404(Ficha, pk=pk)
        filas = Fila.objects.filter(fichas=ficha)
        consulta = Consulta.objects.filter(filas=filas[0])
        autorizacao = Autorizacao.objects.filter(filas=filas[0])
        exame = Exame.objects.filter(filas=filas[0])
        
        if consulta:
            unidade = UnidadeSaude.objects.filter(consultas=consulta[0])
        elif autorizacao:
            unidade = UnidadeSaude.objects.filter(autorizacoes=autorizacao[0])
        else:
            unidade = UnidadeSaude.objects.filter(exames=exame[0])

        tmpJson = serializers.serialize("json", unidade)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

    @action(methods=['get'], detail=True)
    def consulta_unidade(self, request, pk=None):
        consulta = get_object_or_404(Consulta, pk=pk)
        unidade = UnidadeSaude.objects.filter(consultas=consulta)
        tmpJson = serializers.serialize("json", unidade)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


    @action(methods=['get'], detail=True)
    def exame_unidade(self, request, pk=None):
        exame = get_object_or_404(Exame, pk=pk)
        unidade = UnidadeSaude.objects.filter(exames=exame)
        tmpJson = serializers.serialize("json", unidade)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

    
    @action(methods=['get'], detail=True)
    def autorizacao_unidade(self, request, pk=None):
        autorizacao = get_object_or_404(Autorizacao, pk=pk)
        unidade = UnidadeSaude.objects.filter(autorizacoes=autorizacao)
        tmpJson = serializers.serialize("json", unidade)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj)) 

@login_required(login_url='/accounts/login')
def cadastroUnidadeSaude(request):
    form_und = FormUnidadeSaude(request.POST or None, request.FILES or None)
    form_user = FormUser(request.POST or None, request.FILES or None)

    context = {
        'form_und': form_und,
        'form_user': form_user
    }


    if form_und.is_valid() and form_user.is_valid():

        unidade = UnidadeSaude(razao_social=form_und.cleaned_data['razao_social'], telefone=form_und.cleaned_data['telefone'] ,cnpj=form_und.cleaned_data['cnpj'], 
                                logradouro=form_und.cleaned_data['logradouro'], numero=form_und.cleaned_data['numero'], complemento=form_und.cleaned_data['complemento'],
                                bairro=form_und.cleaned_data['bairro'], cidade=form_und.cleaned_data['cidade'], cep=form_und.cleaned_data['cep'],
                                estado=form_und.cleaned_data['estado'], email=request.POST.get('emailUnidade'))

        user = User(username=form_user.cleaned_data['username'], first_name=form_user.cleaned_data['first_name'], last_name=form_user.cleaned_data['last_name'],
                email=request.POST.get('emailUser'))

        user.set_password(form_user.cleaned_data['password'])
        user.save()
        Token.objects.create(user=user)
        unidade.save()
        unidade.users.add(user)
        unidade.save()
        assign_role(user, 'unidade')


        return redirect('listaUnidadeSaudeAdm')

    return render(request, 'cadastro_unidade_saude.html', {'context': context})


@login_required(login_url='/accounts/login')
def alterarUnidadeSaude(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        unidade_saude = get_object_or_404(UnidadeSaude, pk=id)
        user = request.user
        form_und = FormUnidadeSaude(request.POST or None, request.FILES or None, instance=unidade_saude)
        form_user = FormUser(request.POST or None, request.FILES or None, instance=user)

        context = {
            'form_und': form_und,
            'forms_user': form_user
        }
        if form_und.is_valid() and form_user:
            form_user.save()
            form_und.save()
            return redirect('detalhesUnidadeSaude')

        return render(request, 'cadastro_unidade_saude.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def detalhesUnidadeSaude(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        
        context = {
            'unidadeSaude': unidadeSaude,
        }

        return render(request, 'detalhes_unidade_saude.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def detalhesUnidadeAdm(request, id):
    if has_permission(request.user, 'can_add_usuario'):
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        
        context = {
            'unidadeSaude': unidadeSaude,
        }

        return render(request, 'detalhes_unidade_adm.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaConsultasUnidade(request, id):
    if has_permission(request.user, 'permissao_usuario'):  
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        consultas = unidadeSaude.consultas.all().order_by('data', '-create_fila')
        pesquisa = request.GET.get('pesquisa', None)
        espe = Especialista.objects.filter(nome=request.GET.get('pesquisa', None))
        data = request.GET.get('data', None)

        if espe:
            consultas = consultas.filter(especialista__icontains=espe[0]) | consultas.filter(nome__icontains=pesquisa) | consultas.filter(status__icontains=pesquisa)

            if consultas:
                context = {
                    'consultas': consultas,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                consultas = unidadeSaude.consultas.all().order_by('data', '-create_fila')
                context = {
                    'consultas': consultas,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif data:
            consultas = consultas.filter(data=data)

            if consultas:
                context = {
                    'consultas': consultas,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                consultas = unidadeSaude.consultas.all().order_by('data', '-create_fila')
                context = {
                    'consultas': consultas,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif pesquisa:
            consultas = consultas.filter(nome__icontains=pesquisa) | consultas.filter(status__icontains=pesquisa)

            if consultas:
                context = {
                    'consultas': consultas,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                consultas = unidadeSaude.consultas.all().order_by('data', '-create_fila')
                context = {
                    'consultas': consultas,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif consultas:
            context = {
                'consultas': consultas,
                'unidade_aux': unidadeSaude,
            }
        else:
            context = {
                'msg_error': 'Nenhuma consulta cadastrada!'
            }
        
        return render(request, 'lista_consultas_unidade.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaAutorizacoesUnidade(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        autorizacoes = unidadeSaude.autorizacoes.all().order_by('data', '-create_fila')
        pesquisa = request.GET.get('pesquisa')
        resp = Responsavel.objects.filter(nome=request.GET.get('pesquisa', None))
        data = request.GET.get('data', None)

        if resp:
            autorizacoes = autorizacoes.filter(responsavel__icontains=resp[0]).order_by('data', '-create_fila') | autorizacoes.filter(nome__icontains=pesquisa).order_by('data', '-create_fila') | autorizacoes.filter(status__icontains=pesquisa).order_by('data', '-create_fila')
            if autorizacoes:
                context = {
                    'autorizacoes': autorizacoes,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                autorizacoes = unidadeSaude.autorizacoes.all().order_by('data', '-create_fila')
                context = {
                    'autorizacoes': autorizacoes,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif data:
            autorizacoes = autorizacoes.filter(data=data).order_by('data', '-create_fila')
            if autorizacoes:
                context = {
                    'autorizacoes': autorizacoes,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                autorizacoes = unidadeSaude.autorizacoes.all().order_by('data', '-create_fila')
                context = {
                    'autorizacoes': autorizacoes,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif pesquisa:
            autorizacoes = autorizacoes.filter(nome__icontains=pesquisa).order_by('data', '-create_fila') | autorizacoes.filter(status__icontains=pesquisa).order_by('data', 'create_fila')
            if autorizacoes:
                context = {
                    'autorizacoes': autorizacoes,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                autorizacoes = unidadeSaude.autorizacoes.all().order_by('data', '-create_fila')
                context = {
                    'autorizacoes': autorizacoes,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif autorizacoes:
            context = {
                'autorizacoes': autorizacoes,
                'unidade_aux': unidadeSaude,
            }
        else:
            context = {
                'msg_error': 'Nenhuma autorização cadastrada!'
            }

        return render(request, 'lista_autorizacoes_unidade.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaExamesUnidade(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        exames = unidadeSaude.exames.all().order_by('data', '-create_fila')
        pesquisa = request.GET.get('pesquisa', None)
        data = request.GET.get('data', None)

        if data:
            exames = exames.filter(data=data).order_by('data', '-create_fila')
            if exames:
                context = {
                    'exames': exames,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                exames = exames.objects.all().order_by('data', '-create_fila')
                context = {
                    'exames': exames,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif pesquisa:
            exames = exames.filter(nome__icontains=pesquisa).order_by('data', '-create_fila') | exames.filter(status__icontains=pesquisa).order_by('data', '-create_fila') | exames.filter(tipo__icontains=pesquisa).order_by('data', '-create_fila')
            if exames:
                context = {
                    'exames': exames,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                exames = unidadeSaude.exames.all().order_by('data', '-create_fila')
                context = {
                    'exames': exames,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        elif exames:
            context = {
                'exames': exames,
                'unidade_aux': unidadeSaude,
            }
        else:
            context = {
                'msg_error': 'Nenhuma autorização cadastrada!'
            }

        return render(request, 'lista_exames_unidade.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaEspecialistasUnidade(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        especialistas = unidadeSaude.especialistas.all()
        pesquisa = request.GET.get('pesquisa', None)

        if pesquisa:
            profissao = Profissao.objects.filter(nome__icontains=pesquisa)
            especializacao = Especializacao.objects.filter(nome__icontains=pesquisa)
            
            if profissao:
                especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa) | especialistas.filter(profissao__nome__icontains=profissao[0])
                if especialistas:
                    context = {
                        'especialistas': especialistas,
                        'unidade_aux': unidadeSaude,
                        'unidade': unidadeSaude,
                    }
                else:
                    especialistas = unidadeSaude.especialistas.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }

            elif especializacao:
                especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa) | especialistas.filter(especializacao__nome__icontains=especializacao[0])
                if especialistas:
                    context = {
                        'especialistas': especialistas,
                        'unidade_aux': unidadeSaude,
                        'unidade': unidadeSaude,
                    }
                else:
                    especialistas = unidadeSaude.especialistas.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }
            elif pesquisa:
                especialistas = especialistas.filter(nome__icontains=pesquisa) | especialistas.filter(sobrenome__icontains=pesquisa)
                if especialistas:
                    context = {
                        'especialistas': especialistas,
                        'unidade_aux': unidadeSaude,
                        'unidade': unidadeSaude,
                    }
                else:
                    especialistas = unidadeSaude.especialistas.all()
                    context = {
                        'especialistas': especialistas,
                        'msg_busca': 'Nada encontrado para esses parâmetros!'
                    }
        elif especialistas:
            context = {
                'especialistas': especialistas,
                'unidade_aux': unidadeSaude,
            }
        else:
            context = {
                'msg_error': 'Nenhum especialista cadastrado!'
            }
        
        return render(request, 'lista_especialistas_unidade.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaResponsaveisUnidade(request, id):
    if has_permission(request.user, 'permissao_usuario'):
        unidadeSaude = get_object_or_404(UnidadeSaude, pk=id)
        responsaveis = unidadeSaude.responsaveis.all()
        pesquisa = request.GET.get('pesquisa', None)

        if pesquisa:
            
            responsaveis = responsaveis.filter(nome__icontains=pesquisa) | responsaveis.filter(sobrenome__icontains=pesquisa)
            
            if responsaveis:
                context = {
                    'responsaveis': responsaveis,
                    'unidade_aux': unidadeSaude,
                    'unidade': unidadeSaude,
                }
            else:
                responsaveis = unidadeSaude.responsaveis.all()
                context = {
                    'responsaveis': responsaveis,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }

        elif responsaveis:
            context = {
                'responsaveis': responsaveis,
                'unidade_aux': unidadeSaude,
            }
        else:
            context = {
                'msg_error': 'Nenhum responsável cadastrado!'
            }
        
        return render(request, 'lista_responsaveis_unidade.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaUnidadeSaudeUsuario(request):
    if has_permission(request.user, 'permissao_usuario'):
        unidades = UnidadeSaude.objects.all()
        nome = request.GET.get('nome')
        
        if nome:
            unidades = unidades.filter(razao_social__icontains=nome)

            if unidades:
                context = {
                    'unidades': unidades
                }
            else:
                unidades = UnidadeSaude.objects.all()
                context = {
                    'unidades': unidades,
                    'msg_busca': 'Nada encontrado para esses parâmetros!'
                }
        else:
            context = {
                'unidades': unidades
            }
            
        return render(request, 'lista_unidade_saude_usuario.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaUnidadeSaudeAdm(request):
    unidades = UnidadeSaude.objects.all()
    return render(request, 'lista_unidade_saude_adm.html', {'unidades': unidades})

@login_required(login_url='/accounts/login')
def perfilUnidadeSaude(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)

        return render(request, 'perfil_unidade_saude.html', {'unidade': unidade[0]})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def alterarPerfilUnidade(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = get_object_or_404(UnidadeSaude, pk=id)

        if request.method == 'POST':
            try:
                validate_email(request.POST.get('email'))
                valid_email = True
            except ValidationError:
                valid_email = False

            if valid_email:
                unidade.razao_social = request.POST.get('razao_social')
                unidade.cep = request.POST.get('cep')
                unidade.logradouro = request.POST.get('logradouro')
                unidade.numero = request.POST.get('numero')
                unidade.bairro = request.POST.get('bairro')
                unidade.cidade = request.POST.get('cidade')
                unidade.estado = request.POST.get('estado')
                unidade.complemento = request.POST.get('complemento')
                unidade.telefone = request.POST.get('telefone')
                unidade.email = request.POST.get('email')

                unidade.save()

                return render(request, 'perfil_unidade_saude.html', {'unidade': unidade})
            
            else:
                context = {
                    'unidade': unidade,
                    'msg': 'E-mail inválido.'
                }
                return render(request, 'alterar_perfil_unidade.html', {'context': context})
        
        context = {
            'unidade': unidade,
        }

        return render(request, 'alterar_perfil_unidade.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def listaUsuariosUnidade(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)

        context = {
            'unidade': unidade[0],
        }

        return render(request, 'lista_usuarios_unidade.html', {'context': context})
        
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def novoUserUnidade(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
    
        if request.method == 'POST':

            confirm_password = request.POST.get('confirmPassword')
            password = request.POST.get('password')

            if confirm_password == password:

                user = User(username=request.POST.get('username'), first_name=request.POST.get('firstname'), 
                            last_name=request.POST.get('lastname'), email=request.POST.get('email'))
                user.set_password(request.POST.get('password'))

                user.save()
                Token.objects.create(user=user)
                unidade[0].users.add(user)
                unidade[0].save()
                assign_role(user, 'unidade')

                unidade = UnidadeSaude.objects.filter(users=request.user)

                context = {
                    'unidade': unidade[0],
                }

                return render(request, 'lista_usuarios_unidade.html', {'context': context})
            else:
                msg = 'Senhas não conferem.'
                return render(request, 'novo_user_unidade.html', {'msg': msg})

        return render(request, 'novo_user_unidade.html')
    
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

