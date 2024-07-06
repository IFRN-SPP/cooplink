from django.urls import path
from app.views.institution import (
    InstitutionList,
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionDelete,
    InstitutionDetail,
)

# Adicione suas URLs aqui
urlpatterns = [
    path('', InstitutionList.as_view(), name='institution-list'),
    path('js/create/institution/', InstitutionCreate.as_view(), name='js-create-institution'),
    path('js/update/institution/<int:pk>/', InstitutionUpdate.as_view(), name='js-update-institution'),
    path('js/delete/institution/<int:pk>/', InstitutionDelete.as_view(), name='js-delete-institution'),
    path('<int:pk>/detalhar/',  InstitutionDetail, name='detail-institution'),
]