from django.shortcuts import render, redirect
from .models import *
import uuid
from .utils import filtrar_produtos, preco_minino_maximo
from django.db.models import Max, Min


# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, "homepage.html", context)


def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrar_produtos(produtos, filtro)
    if request.method == "POST":
        dados = request.POST.dict()
        produtos = produtos.filter(
            preco__gte=dados.get("preco_minimo"), preco__lte=dados.get("preco_maximo")
        )
        if "tamanho" in dados:
            itens = ItemEstoque.objects.filter(
                produto__in=produtos, tamanho=dados.get("tamanho")
            )
            ids_produtos = itens.values_list("produto", flat=True).distinct()
            produtos = produtos.filter(id__in=ids_produtos)
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list("tamanho", flat=True).distinct()
    minimo, maximo = preco_minino_maximo(produtos)
    context = {
        "Produtos": produtos,
        "minimo": minimo,
        "maximo": maximo,
        "tamanhos": tamanhos,
    }
    return render(request, "loja.html", context)


def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = {}
    tamanhos = {}
    nome_cor = None
    if id_cor:
        nome_cor = Cor.objects.get(id=id_cor)
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    if len(itens_estoque) > 0:
        tem_estoque = True
        cores = {item.cor for item in itens_estoque}
        if id_cor:
            itens_estoque = ItemEstoque.objects.filter(
                produto=produto, quantidade__gt=0, cor__id=id_cor
            )
            tamanhos = {item.tamanho for item in itens_estoque}
    context = {
        "produto": produto,
        "tem_estoque": tem_estoque,
        "cores": cores,
        "tamanhos": tamanhos,
        "nome_cor": nome_cor,
    }
    return render(request, "ver_produto.html", context)


def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect("loja")
        resposta = redirect("carrinho")
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
            else:
                id_sessao = str(uuid.uuid4)
                resposta.set_cookie(
                    key="id_sessao", value=id_sessao, max_age=60 * 60 * 24 * 30
                )
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(
            produto__id=id_produto, tamanho=tamanho, cor__id=id_cor
        )
        item_pedido, criado = ItensPedido.objects.get_or_create(
            item_estoque=item_estoque, pedido=pedido
        )
        item_pedido.quantidade += 1
        item_pedido.save()
        return resposta
    else:
        return redirect("loja")


def remover_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:
            return redirect("loja")
        resposta = redirect("carrinho")
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
            else:
                id_sessao = str(uuid.uuid4)
                resposta.set_cookie(
                    key="id_sessao", value=id_sessao, max_age=60 * 60 * 24 * 30
                )
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(
            produto__id=id_produto, tamanho=tamanho, cor__id=id_cor
        )
        item_pedido, criado = ItensPedido.objects.get_or_create(
            item_estoque=item_estoque, pedido=pedido
        )
        item_pedido.quantidade -= 1
        item_pedido.save()
        if item_pedido.quantidade <= 0:
            item_pedido.delete()
        return redirect("carrinho")
    else:
        return redirect("loja")


def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {"cliente_existente": False, "itens_pedido": None, "pedido": None}
            return render(request, "carrinho.html", context)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    context = {
        "itens_pedido": itens_pedido,
        "pedido": pedido,
        "cliente_existente": True,
    }
    return render(request, "carrinho.html", context)


def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao = request.COOKIES.get("id_sessao")
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect("loja")
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {
        "pedido": pedido,
        "enderecos": enderecos,
    }
    return render(request, "checkout.html", context)


def adicionar_endereco(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao = request.COOKIES.get("id_sessao")
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect("loja")
        dados = request.POST.dict()
        endereco = Endereco.objects.create(
            cliente=cliente,
            cidade=dados.get("cidade"),
            estado=dados.get("estado"),
            rua=dados.get("rua"),
            numero=int(dados.get("numero")),
            complemento=dados.get("complemento"),
            cep=dados.get("cep"),
        )
        endereco.save()
        return redirect("checkout")
    else:
        context = {}
        return render(request, "adicionar_endereco.html", context)


def minha_conta(request):
    return render(request, "usuarios/minhaconta.html")


def login(request):
    return render(request, "usuarios/login.html")
