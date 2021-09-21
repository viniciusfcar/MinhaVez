from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Responsavel
from .forms import FormResponsavel
from unidadeSaude.models import UnidadeSaude
from rest_framework import viewsets
from .serializers import ReponsavelSerializer
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from rolepermissions.checkers import has_permission
from datetime import date


class GetResponsavelViewSet(viewsets.ModelViewSet):
    queryset = Responsavel.objects.all()
    serializer_class = ReponsavelSerializer

@login_required(login_url='/accounts/login')
def cadastroResponsavel(request):
    if has_permission(request.user, 'permissao_unidade'):
        form = FormResponsavel(request.POST or None, request.FILES or None)

        if form.is_valid():
            responsavel = Responsavel(nome=form.cleaned_data['nome'], sobrenome=form.cleaned_data['sobrenome'], imagem=request.FILES['imagem'])
            responsavel.user = request.user
            responsavel.save()
            unidade = UnidadeSaude.objects.filter(users=request.user)
            if unidade:
                unidade[0].responsaveis.add(responsavel)
                unidade[0].save()
            return redirect('listaResponsavel')

        return render(request, 'cadastro_responsavel.html', {'form': form})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def listaResponsavel(request):
    if has_permission(request.user, 'permissao_unidade'):
        unidade = UnidadeSaude.objects.filter(users=request.user)
        pesquisa = request.GET.get('pesquisa')
        data = date.today()

        if unidade:
            responsaveis = unidade[0].responsaveis.all()

            if pesquisa:
                responsaveis = responsaveis.filter(nome__icontains=pesquisa) | responsaveis.filter(sobrenome__icontains=pesquisa)
                
                if responsaveis:
                    context = {
                        'responsaveis': responsaveis,
                        'data': data
                    }
                else:
                    responsaveis = unidade[0].responsaveis.all()
                    context = {
                        'responsaveis': responsaveis,
                        'msg_busca': 'Nada encontrado para esses parâmetros!',
                        'data': data
                    }
            elif responsaveis:
                context = {
                    'responsaveis': responsaveis,
                    'data': data
                }
            else:
                context = {
                    'msg_alert': 'Ainda não possuem Responsáveis cadastrados!'
                }

            contexto.set(context)

            return render(request, 'lista_responsavel.html', {'context': context})

        else:
            context = {
                'msg_error': 'Indisponivel Acessar Essa Área'

            }
            return redirect('home_unidade_saude.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


@login_required(login_url='/accounts/login')
def alterarResponsavel(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        responsavel = get_object_or_404(Responsavel, pk=id)
        form = FormResponsavel(request.POST or None, request.FILES or None, instance=responsavel)
        
        if form.is_valid():
            form.save()
            return redirect('listaResponsavel')

        return render(request, 'cadastro_responsavel.html', {'form': form})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def deleteResponsavel(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        responsavel = get_object_or_404(Responsavel, pk=id)
        form = FormResponsavel(request.POST or None, request.FILES or None, instance=responsavel)

        if request.method == 'POST':
            responsavel.delete()
            return redirect('listaResponsavel')

        return render(request, 'delete_responsavel.html', {'nome': responsavel.nome})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def relatorioResponsavel(request):
    if has_permission(request.user, 'permissao_unidade'):
        html_string = render_to_string('relatorio_responsavel.html', {'context': contexto.get()})
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        html.write_pdf(target='/tmp/relatorio_responsavel.pdf', presentational_hints=True)
        fs = FileSystemStorage('/tmp')

        with fs.open('relatorio_responsavel.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio_responsavel.pdf'
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