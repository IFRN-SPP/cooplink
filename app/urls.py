from django.urls import path
from .views import *

# Adicione suas URLs aqui
urlpatterns = [
    path("", index, name="index"),

    # CRUD Instituição com Ajax
    path('instituicoes/', InstitutionList.as_view(), name='institution-list'),
    path('js/create/institution/', InstitutionCreate.as_view(), name='js-create-institution'),
    path('js/update/institution/<int:pk>/', InstitutionUpdate.as_view(), name='js-update-institution'),
    path('js/delete/institution/<int:pk>/', InstitutionDelete.as_view(), name='js-delete-institution'),

    # CRUD Produtos com Ajax
    path("produtos/", ProductList.as_view(), name="product-list"),
    path("js/create/product/", ProductCreate.as_view(), name="js-create-product"),
    path("js/update/product/<int:pk>", ProductUpdate.as_view(), name="js-update-product"),
    path("js/delete/product/<int:pk>", ProductDelete.as_view(), name="js-delete-product"),

]