from django.shortcuts import render
from .models import *


# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, "homepage.html", context)


def loja(request, nome_categoria=None):
    produtos = Produto.objects.filter(ativo=True)
    if nome_categoria:
        produtos = produtos.filter(categoria__nome=nome_categoria)
    context = {"Produtos": produtos}
    return render(request, "loja.html", context)


def ver_produto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    context = {"produto": produto}
    return render(request, "ver_produto.html", context)


def carrinho(request):
    return render(request, "carrinho.html")


def checkout(request):
    return render(request, "checkout.html")


def minha_conta(request):
    return render(request, "usuarios/minhaconta.html")


def login(request):
    return render(request, "usuarios/login.html")
