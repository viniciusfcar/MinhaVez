from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from unidadeSaude.models import UnidadeSaude
from usuario.models import Usuario
from django.contrib.auth.models import User
from ficha.models import Ficha
from fila.models import Fila
from responsavel.models import Responsavel
from rolepermissions.checkers import has_permission
from django.core.validators import validate_email

@login_required(login_url='/accounts/login')
def configuracoes_unidade(request):

    if has_permission(request.user, 'permissao_unidade'):

        unidade = UnidadeSaude.objects.filter(users=request.user)

        return render(request, 'configuracoes_unidade.html', {'unidade': unidade[0]})
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('homeUsuario', {'context': context})

@login_required(login_url='/accounts/login')
def configuracoesUsuario(request):

    if has_permission(request.user, 'permissao_usuario'):

        usuario = Usuario.objects.get(user=request.user)

        return render(request, 'configuracoes_usuario.html', {'usuario': usuario})
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('home', {'context': context})

@login_required(login_url='/accounts/login')
def alterarUsernameUsuario(request):
    
    if has_permission(request.user, 'permissao_usuario'):
        if request.method == 'POST':

            try:
                user = User.objects.get(username=request.POST.get('username'))
            except:
                user = None

            if user == request.user:

                user.username = request.POST.get('newUsername')
                user.save()

                context = {
                    'msg': 'Username alterado com sucesso.'
                }
                return render(request, 'configuracoes_usuario.html', {'context': context})
            
            else:
                context = {
                    'msg': 'Você está tentando alterar o username de outro Usuário ou um que Não Existe.'
                }

                return render(request, 'alterar_username_usuario.html', {'context': context})

        return render(request, 'alterar_username_usuario.html')
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('home', {'context': context})

@login_required(login_url='/accounts/login')
def alterarEmailUsuario(request):
    
    if has_permission(request.user, 'permissao_usuario'):
        if request.method == 'POST':

            try:
                user = User.objects.get(email=request.POST.get('email'))
            except:
                user = None
            
            if user == request.user:
                try:
                    validate_email(request.POST.get('newEmail'))
                    valid_email = True
                except:
                    valid_email = False
                
                if valid_email:
                    user.email = request.POST.get('newEmail')
                    user.save()

                    context = {
                        'msg': 'E-mail alterado com sucesso.'
                    }
                    return render(request, 'configuracoes_usuario.html', {'context': context})
                
                else:
                    context = {
                        'msg': 'Preencha um novo e-mail válido.'
                    }

                    return render(request, 'alterar_email_usuario.html', {'context': context})
            
            else:
                context = {
                    'msg': 'Você está tentando alterar o e-mail de outro Usuário ou um que Não Existe.'
                }

                return render(request, 'alterar_email_usuario.html', {'context': context})

        return render(request, 'alterar_email_usuario.html')
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('home', {'context': context})

@login_required(login_url='/accounts/login')
def alterarEmailUserUnidade(request):
    
    if has_permission(request.user, 'permissao_unidade'):
        if request.method == 'POST':

            try:
                user = User.objects.get(email=request.POST.get('email'))
            except:
                user = None
            
            if user == request.user:
                try:
                    validate_email(request.POST.get('newEmail'))
                    valid_email = True
                except:
                    valid_email = False
                
                if valid_email:
                    user.email = request.POST.get('newEmail')
                    user.save()

                    context = {
                        'msg': 'E-mail alterado com sucesso.'
                    }
                    return render(request, 'configuracoes_unidade.html', {'context': context})
                
                else:
                    context = {
                        'msg': 'Preencha um novo e-mail válido.'
                    }

                    return render(request, 'alterar_email_user_unidade.html', {'context': context})
            
            else:
                context = {
                    'msg': 'Você está tentando alterar o e-mail de outro Usuário ou um que Não Existe.'
                }

                return render(request, 'alterar_email_user_unidade.html', {'context': context})

        return render(request, 'alterar_email_user_unidade.html')
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('home', {'context': context})

@login_required(login_url='/accounts/login')
def alterarUsernameUserUnidade(request):
    
    if has_permission(request.user, 'permissao_unidade'):
        if request.method == 'POST':

            try:
                user = User.objects.get(username=request.POST.get('username'))
            except expression as identifier:
                user = None

            if user == request.user:

                user.username = request.POST.get('newUsername')
                user.save()

                context = {
                    'msg': 'Username alterado com sucesso.'
                }
                return render(request, 'configuracoes_unidade.html', {'context': context})
            
            else:
                context = {
                    'msg': 'Você está tentando alterar o username de outro Usuário ou um que Não Existe..'
                }

                return render(request, 'alterar_username_user_unidade.html', {'context': context})

        return render(request, 'alterar_username_user_unidade.html')
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('homeUsuario', {'context': context})

@login_required(login_url='/accounts/login')
def alterarSenhaUserUnidade(request):

    if has_permission(request.user, 'permissao_unidade'):
        if request.method == 'POST':
            user = User.objects.get(username=request.user.username)
            atual_password = request.POST.get('atualPassword')
            password = request.POST.get('password')
            confirm_passowrd = request.POST.get('confirmPassword')
            

            if password != confirm_passowrd:
                context = {
                    'msg': 'A nova senha está diferente do campo de confirmação.'
                }
                return render(request, 'alterar_senha_user_unidade.html', {'msg': msg})
            
            elif not user.check_password(atual_password):
                context = {
                    'msg': 'Senha atual não confere com a cadastrada.'
                }
                return render(request, 'alterar_senha_user_unidade.html', {'context': context})
            
            else:
                user.set_password(password)
                user.save()

                context = {
                    'msg': 'Senha redefinida com sucesso.'
                }
                return render(request, 'configuracoes_unidade.html', {'context': context})

        return render(request, 'alterar_senha_user_unidade.html')
    
    else:
        context = {
            'msg_error': 'Sem Permissão Para Essa Área'

        }
        return redirect('homeUsuario', {'context': context})