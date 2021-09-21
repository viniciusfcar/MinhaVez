from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profissao
from .forms import FormProfissao
from rest_framework import viewsets
from .serializers import ProfissaoSerializer


class GetProfissaoViewSet(viewsets.ModelViewSet):
    queryset = Profissao.objects.all()
    serializer_class = ProfissaoSerializer


@login_required
def cadastroProfissao(request):
    form = FormProfissao(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('listaPessoas')

    return render(request, 'cadastro_profissao.html', {'form': form})


@login_required
def listaProfissao(request):
    profissoes = Profissao.objects.all()

    return render(request, 'lista_profissoes.html', {'profissoes': profissoes})


@login_required
def alterarProfissao(request, id):
    profissao = get_object_or_404(Profissao, pk=id)
    form = FormProfissao(request.POST or None, request.FILES or None, instance=profissao)

    if form.is_valid():
        form.save()
        return redirect('listaPessoas')

    return render(request, 'cadastro_profissao.html', {'form': form})


@login_required
def deleteProfissao(request, id):
    profissao = get_object_or_404(Profissao, pk=id)
    form = FormProfissao(request.POST or None, request.FILES or None, instance=profissao)

    if request.method == 'POST':
        profissao.delete()
        return redirect('listaProfissao')

    return render(request, 'delete_profissao.html', {'nome': profissao.nome})