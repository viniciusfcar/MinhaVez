from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from unidadeSaude.models import UnidadeSaude
from usuario.models import Usuario
from rolepermissions.checkers import has_permission
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == 'POST':

        try:
            user = User.objects.get(username=username)

            if user is None:
                msg_error = 'Usuário inválido(s)'
                return render(request, 'login.html', {'msg_error': msg_error})
            else:

                if not user.check_password(password):
                    msg_error = 'Senha inválida'
                    return render(request, 'login.html', {'msg_error': msg_error})
                else:
                    user = authenticate(username=username, password=password)
                    auth_login(request, user)

                    if has_permission(user, 'can_add_usuario'):
                        return redirect('homeAdm')

                    elif has_permission(user, 'permissao_usuario'):
                        return redirect('homeUsuario')
                    
                    elif has_permission(user, 'permissao_unidade'):
                        return redirect('homeUnidadeSaude')
                        
        except Exception:
            msg_error = 'Usuário e/ou Senha inválido(s)'
            return render(request, 'login.html', {'msg_error': msg_error})

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            try:
                usuario = Usuario.objects.get(cpf=request.POST.get('cpf'))
                associated_users = User.objects.filter(Q(email=data))

                if associated_users.exists() and usuario.user.email.lower() == data.lower():
                    for user in associated_users:
                        context = {
                            'domain':'https://minhavezsistema.com.br/accounts/password_reset_confirm/',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            'user': user,
                        }
                        email = render_to_string('recuperar_senha.txt', {'context': context})
                        send_mail(
                            'Recuperar Senha',
                            email,
                            'minhavezsistema@gmail.com',
                            [data],
                        )
                        return render(request, 'password_reset_none.html')
                else:
                    context ={
                        'msg_error': 'Tente novamente!'
                    }
                    return render(request=request, template_name="password_reset.html", context={'context': context})
            except:
                context ={
                    'msg_error': 'Tente novamente!'
                }
                return render(request=request, template_name="password_reset.html", context={'context': context}) 
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})


