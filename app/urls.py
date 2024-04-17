from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

# Adicione suas URLs aqui
urlpatterns = [
    path("", index, name="index"),

    # Autenticação
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # CRUD Instituição com Ajax
    path('instituicoes/', InstitutionList.as_view(), name='institution-list'),
    path('js/create/institution/', InstitutionCreate.as_view(), name='js-create-institution'),
    path('js/update/institution/<int:pk>/', InstitutionUpdate.as_view(), name='js-update-institution'),
    path('js/delete/institution/<int:pk>/', InstitutionDelete.as_view(), name='js-delete-institution'),

    # CRUD Produtos com Ajax
    path("produtos/", ProductList.as_view(), name="product-list"),
    path("js/create/product/", ProductCreate.as_view(), name="js-create-product"),
    path("js/update/product/<int:pk>/", ProductUpdate.as_view(), name="js-update-product"),
    path("js/delete/product/<int:pk>/", ProductDelete.as_view(), name="js-delete-product"),

    # CRUD Usuáro com Ajax
    path("usuarios/", UserList.as_view(), name="user-list"),
    path("js/create/user/", UserCreate.as_view(), name="js-create-user"),
    path("js/update/user/<int:pk>/", UserUpdate.as_view(), name="js-update-user"),
    path("js/delete/user/<int:pk>/", UserDelete.as_view(), name="js-delete-user"),
    # Update de infos do Usuário
    path("usuario/<int:pk>/mudar-senha/", UserUpdatePassword.as_view(), name="update-user-password"),
    path("usuario/<int:pk>/mudar-permissao", UserUpdatePermission.as_view(), name="update-user-permission"),

    # CRUD Call - Padrão Django
    path('chamadas/', CallList.as_view(), name= 'call-list'),
    path('cadastrar/chamada/', CallCreate, name='create-call'),
    path('detalhar/<int:pk>/chamada/', CallDetail, name='detail-call'),
    path('atualizar/<int:pk>/chamada/', CallUpdate.as_view(), name='update-call'),
    path('deletar/<int:pk>/chamada/', CallDelete.as_view(), name='delete-call'),

    # CRUD Call Product 
    path('produtos-chamadas/delete/<int:pk>/', CallProductDelete, name= 'delete-call-product'),
    path('produtos-chamadas/update/<int:pk>/', CallProductUpdate, name= 'update-call-product'),

    # CRUD Pedidos e Produtos dos pedidos
    path('pedidos/', OrderList, name= 'order-list'),
    path('cadastrar/pedido/', OrderCreate, name='create-order'),
    path('administacao/cadastrar/pedido/', OrderCreateAdmin, name= 'create-order-admin'),
    path('detalhar/<int:pk>/pedido/', OrderDetail, name='detail-order'),
    path('deletar/<int:pk>/pedido/', OrderDelete, name='delete-order'),
    # view para chamadas ajax 
    path('get_products/', get_products, name='get_products'),
    path('get_calls/', get_calls, name='get_calls'),

]