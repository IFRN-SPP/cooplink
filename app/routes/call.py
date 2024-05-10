from django.urls import path
from app.views.call import (
    CallList,
    CallCreate,
    CallDetail,
    CallUpdate,
    CallUpdateActive,
    CallDelete,
    CallProductDelete,
    CallProductUpdate
)

# Adicione suas URLs aqui
urlpatterns = [
    # CRUD Call
    path('', CallList.as_view(), name= 'call-list'),
    path('cadastrar/', CallCreate, name='create-call'),
    path('<int:pk>/detalhar/', CallDetail, name='detail-call'),
    path('<int:pk>/atualizar/', CallUpdate.as_view(), name='update-call'),
    path('<int:pk>/atualizar/situacao/', CallUpdateActive, name='update-call-active'),
    path('js/<int:pk>/deletar/', CallDelete.as_view(), name='js-delete-call'),

    # CRUD Call Product
    path('<int:pk>/deletar/produtos/', CallProductDelete, name= 'delete-call-product'),
    path('<int:pk>/atualizar/produtos/', CallProductUpdate, name= 'update-call-product'),
]