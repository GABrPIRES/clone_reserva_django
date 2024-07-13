from django.urls import path

# from . import views -> Poderia ser assim
from .views import *

urlpatterns = [
    # path('', views.homepage) -> Poderia ser assim
    path("", homepage, name="homepage"),
    path("loja/", loja, name="loja"),
    path("minhaconta/", minha_conta, name="minha_conta"),
    path("login/", login, name="login"),
    path("carrinho/", carrinho, name="carrinho"),
    path("checkout/", checkout, name="checkout"),
]
