from django.urls import path
from .views import CallList, CallCreate, CallDetail, CallUpdate, CallDelete, CallProductDelete, CallProductUpdate

# Adicione suas URLs aqui
urlpatterns = [
    # CRUD Call 
    path('', CallList, name= 'call-list'),
    path('cadastrar/', CallCreate, name='create-call'),
    path('<int:pk>/detalhar/', CallDetail, name='detail-call'),
    path('<int:pk>/atualizar/', CallUpdate.as_view(), name='update-call'),
    path('<int:pk>/deletar/', CallDelete.as_view(), name='delete-call'),

    # CRUD Call Product 
    path('<int:pk>/deletar/produtos/', CallProductDelete, name= 'delete-call-product'),
    path('<int:pk>/atualizar/produtos/', CallProductUpdate, name= 'update-call-product'),
]