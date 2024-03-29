from django.urls import path
from .views import *

# Adicione suas URLs aqui
urlpatterns = [
    path("", index, name="index"),

    # CRUD Instituição com Ajax
    path('instituicoes/', InstitutionList.as_view(), name='institution-list'),
    path('js/create/institution/', InstitutionCreate.as_view(), name='js-create-institution'),
    path('js/update/<int:pk>/', InstitutionUpdate.as_view(), name='js-update-institution'),
    path('js/delete/<int:pk>/', InstitutionDelete.as_view(), name='js-delete-institution'),
]