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
    path('create/call/', CallCreate.as_view(), name='call-create'),
    path('update/call/<int:pk>/', CallUpdate.as_view(), name='update-call'),
    path('delete/call/<int:pk>/', CallDelete.as_view(), name='delete-call'),
]