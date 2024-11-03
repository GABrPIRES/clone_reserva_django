import mercadopago

public_key = "APP_USR-75c13315-3acc-4900-93a3-879747b9e564"
token = "APP_USR-2568573785496441-110122-09fe54c46b21ae20d513db3eb8878570-2073438676"


def criar_pagamento(itens_pedido, link):

    sdk = mercadopago.SDK(token)

    itens = []
    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = item.item_estoque.produto.nome
        preco_unitario = float(item.item_estoque.produto.preco)
        itens.append(
            {
                "title": nome_produto,
                "quantity": quantidade,
                "unit_price": preco_unitario,
            }
        )

    preference_data = {
        "items": itens,
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link,
        },
    }

    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]
    id_pagamento = resposta["response"]["id"]
    return link_pagamento, id_pagamento
