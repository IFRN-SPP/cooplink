from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from .views import index
from .order.views import get_calls, get_products, get_balance

from .institution import urls as institution
from .user import urls as user
from .product import urls as product
from .call import urls as call
from .order import urls as order

# Adicione suas URLs aqui
urlpatterns = [
    path("", index, name="index"),

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