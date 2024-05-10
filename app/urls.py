from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from .views.index import index, index_admin
from .views.order import get_calls, get_products, get_balance

from .routes import institution, user, product, call, order

# Adicione suas URLs aqui
urlpatterns = [
    path("", index, name="index"),
    path("administracao/", index_admin, name="index-admin"),

    # Autenticação
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Objetos
    path('instituicoes/', include(institution)),
    path('usuarios/', include(user)),
    path('produtos/', include(product)),
    path('chamadas/', include(call)),
    path('pedidos/', include(order)),

    # view para chamadas ajax
    path('get_products/', get_products, name='get_products'),
    path('get_calls/', get_calls, name='get_calls'),
    path('get_balance/', get_balance, name='get_balance'),

]