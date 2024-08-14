from django.db.models import Min, Max


def filtrar_produtos(produtos, filtro):
    if filtro:
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos


def preco_minino_maximo(produtos):
    minimo = 0
    maximo = 0
    if len(produtos) > 0:
        minimo = round(list(produtos.aggregate(Min("preco")).values())[0], 2)
        maximo = round(list(produtos.aggregate(Max("preco")).values())[0], 2)

    return minimo, maximo
