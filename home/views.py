from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rolepermissions.checkers import has_permission
from consulta.models import Consulta
from autorizacao.models import Autorizacao
from ficha.models import Ficha
from fila.models import Fila
from exame.models import Exame
from datetime import date
from usuario.models import Usuario
from notificacoes import views as notificacoes


@login_required(login_url='/accounts/login')
def homeUnidadeSaude(request):
    if has_permission(request.user, 'permissao_unidade'):
        return render(request, 'home.html')
    else:
        return redirect('homeUsuario')


@login_required(login_url='/accounts/login')
def homeUsuario(request):
    if has_permission(request.user, 'permissao_usuario'):
        usuario = Usuario.objects.filter(user=request.user)
        return render(request, 'home_usuario.html', {'usuario': usuario[0]})
    else:
        return redirect('homeUnidadeSaude')


@login_required(login_url='/accounts/login')
def homeAdm(request):
    if has_permission(request.user, 'can_add_usuario'):
        return render(request, 'home_adm.html')
    else:
        return (redirect('/'))

@login_required(login_url='/accounts/login')
def filasIniciadas(request):
    if has_permission(request.user, 'permissao_unidade'):    
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        if consultas_iniciadas or autorizacoes_iniciadas:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
            }
        elif exames_iniciadas:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
            }
        else:
            context = {
                'msg_error': 'Não possue filas iniciadas para hoje!'
            }
            
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def chamarFichaNormalConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):  
        consulta = get_object_or_404(Consulta, pk=id)
        fila_normal = None
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        for fila in consulta.filas.all():
            if fila.fila_preferencial != True:
                fila_normal = fila
        
        if fila_normal.fichas.all():
            for ficha in fila_normal.fichas.all().order_by('numero'):
                if ficha.status == "AGUARDANDO":
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'ficha': ficha
                    }

                    #NOTIFICAÇÂO
                    notificacoes.avisaPosicaoFila(request, fila_normal)
                    
                    return render(request, 'filas_iniciadas.html', {'context': context})
                else:
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'msg_ficha': "Acabaram as fichas dessa fila!"
                    }
        else:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
                'msg_ficha': "Não existem fichas para essa fila!"
            }
        
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def chamarFichaPreferencialConsulta(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        consulta = get_object_or_404(Consulta, pk=id)
        fila_preferencial = None
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        for fila in consulta.filas.all():
            if fila.fila_preferencial == True:
                fila_preferencial = fila

        if fila_preferencial.fichas.all():
            for ficha in fila_preferencial.fichas.all().order_by('numero'):
                if ficha.status == "AGUARDANDO":
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'ficha': ficha
                    }
                    
                    #NOTIFICAÇÂO
                    notificacoes.avisaPosicaoFila(request, fila_preferencial)
                    
                    return render(request, 'filas_iniciadas.html', {'context': context})
                else:
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'msg_ficha': "Acabaram as fichas dessa fila!"
                    }
        else:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
                'msg_ficha': "Não existem fichas para essa fila!"
            }
        
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def chamarFichaNormalAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):  
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        fila_normal = None
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        for fila in autorizacao.filas.all():
            if fila.fila_preferencial != True:
                fila_normal = fila
        
        if fila_normal.fichas.all():
            for ficha in fila_normal.fichas.all().order_by('numero'):
                if ficha.status == "AGUARDANDO":
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'ficha': ficha
                    }

                    #NOTIFICAÇÂO
                    notificacoes.avisaPosicaoFila(request, fila_normal)
                    
                    return render(request, 'filas_iniciadas.html', {'context': context})
                else:
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'msg_ficha': "Acabaram as fichas dessa fila!"
                    }
        else:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
                'msg_ficha': "Não existem fichas para essa fila!"
            }
        
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def chamarFichaPreferencialAutorizacao(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        autorizacao = get_object_or_404(Autorizacao, pk=id)
        fila_preferencial = None
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        for fila in autorizacao.filas.all():
            if fila.fila_preferencial == True:
                fila_preferencial = fila

        if fila_preferencial.fichas.all():
            for ficha in fila_preferencial.fichas.all().order_by('numero'):
                if ficha.status == "AGUARDANDO":
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'ficha': ficha
                    }

                    #NOTIFICAÇÂO
                    notificacoes.avisaPosicaoFila(request, fila_preferencial)
                    
                    return render(request, 'filas_iniciadas.html', {'context': context})
                else:
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'msg_ficha': "Acabaram as fichas dessa fila!"
                    }
        else:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
                'msg_ficha': "Não existem fichas para essa fila!"
            }
        
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

#----------------------------------
@login_required(login_url='/accounts/login')
def chamarFichaNormalExame(request, id):
    if has_permission(request.user, 'permissao_unidade'):  
        exame = get_object_or_404(Exame, pk=id)
        fila_normal = None
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        for fila in exame.filas.all():
            if fila.fila_preferencial != True:
                fila_normal = fila
        
        if fila_normal.fichas.all():
            for ficha in fila_normal.fichas.all().order_by('numero'):
                if ficha.status == "AGUARDANDO":
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'ficha': ficha
                    }

                    #NOTIFICAÇÂO
                    notificacoes.avisaPosicaoFila(request, fila_normal)
                    
                    return render(request, 'filas_iniciadas.html', {'context': context})
                else:
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'msg_ficha': "Acabaram as fichas dessa fila!"
                    }
        else:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
                'msg_ficha': "Não existem fichas para essa fila!"
            }
        
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def chamarFichaPreferencialExame(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        exame = get_object_or_404(Exame, pk=id)
        fila_preferencial = None
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)
        
        for fila in exame.filas.all():
            if fila.fila_preferencial == True:
                fila_preferencial = fila

        if fila_preferencial.fichas.all():
            for ficha in fila_preferencial.fichas.all().order_by('numero'):
                if ficha.status == "AGUARDANDO":
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'ficha': ficha
                    }

                    #NOTIFICAÇÂO
                    notificacoes.avisaPosicaoFila(request, fila_preferencial)
                    
                    return render(request, 'filas_iniciadas.html', {'context': context})
                else:
                    context = {
                        "consultas_iniciadas": consultas_iniciadas,
                        "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                        'msg_ficha': "Acabaram as fichas dessa fila!"
                    }

        else:
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                        "exames_iniciadas": exames_iniciadas,
                'msg_ficha': "Não existem fichas para essa fila!"
            }
        
        return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def atenderFicha(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        ficha = get_object_or_404(Ficha, pk=id)
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)

        if request.method == 'POST':
            ficha.status = "ATENDIDA"
            ficha.save()
            
            context = {
                "consultas_iniciadas": consultas_iniciadas,
                "autorizacoes_iniciadas": autorizacoes_iniciadas,
                "exames_iniciadas": exames_iniciadas,
            }  
            return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})

@login_required(login_url='/accounts/login')
def pularFicha(request, id):
    if has_permission(request.user, 'permissao_unidade'):
        ficha = get_object_or_404(Ficha, pk=id)
        fila = Fila.objects.get(fichas=ficha)
        hoje = date.today()
        consultas_iniciadas = Consulta.objects.filter(status="INICIADA", data=hoje)
        autorizacoes_iniciadas = Autorizacao.objects.filter(status="INICIADA", data=hoje)
        exames_iniciadas = Exame.objects.filter(status="INICIADA", data=hoje)

        if request.method == 'POST':
            num_ficha = ficha.numero + 1
            ficha_new = None

            for fic in fila.fichas.all().order_by('numero'):
                if fic.numero == num_ficha:
                    ficha_new = fic
            
            if ficha_new:
                context = {
                    "consultas_iniciadas": consultas_iniciadas,
                    "autorizacoes_iniciadas": autorizacoes_iniciadas,
                    "exames_iniciadas": exames_iniciadas,
                    "ficha": ficha_new,
                }

                return render(request, 'filas_iniciadas.html', {'context': context})
            
            else:
                context = {
                    "consultas_iniciadas": consultas_iniciadas,
                    "autorizacoes_iniciadas": autorizacoes_iniciadas,
                    "exames_iniciadas": exames_iniciadas,
                    "msg_ficha": 'Não tem mais fichas após essa.',
                }

                return render(request, 'filas_iniciadas.html', {'context': context})
    else:
        context = {
            'msg_error': 'Impossivel Acessar Essa Área'
        }
        return render(request, 'home_usuario.html', {'context': context})


    