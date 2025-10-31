from django.urls import path
from app.views.order import (
  OrderList,
  OrderCreate,
  OrderCreateAdmin,
  OrderDetail,
  OrderDelete,
  OrderedProductDelete,
  OrderedProductUpdate,
  EvaluateOrder,
  EvaluateOrderDenied,
  ReopenOrder,
  OrderDelivered,
  OrderReport,
  WeekReport,
  RequestReport,
)

# Adicione suas URLs aqui
urlpatterns = [
    # CRUD Pedidos e Produtos dos pedidos
    path('', OrderList.as_view(), name= 'order-list'),
    path('cadastrar/', OrderCreate, name='create-order'),
    path('administracao/cadastrar/', OrderCreateAdmin, name= 'create-order-admin'),
    path('<int:pk>/detalhar/', OrderDetail, name='detail-order'),
    path('js/<int:pk>/deletar/', OrderDelete.as_view(), name='js-delete-order'),
    # deleta os produtos que estão nos pedidos
    path("<int:pk>/deletar/produtos/",  OrderedProductDelete, name="delete-ordered-product"),
    path("<int:pk>/atualizar/produtos/", OrderedProductUpdate, name="update-ordered-product"),
    # avaliar pedido
    path('<int:pk>/avaliar/', EvaluateOrder, name='evaluate-order'),
    path('<int:pk>/negar/', EvaluateOrderDenied, name='denied-order'),
    path('<int:pk>/reabrir/', ReopenOrder, name='reopen-order'),
    # confirmação de entrega
    path('<int:pk>/confirmar-entrega/',OrderDelivered, name='order-delivered'),
    path('relatorio/semanal/', WeekReport, name='week-report'),
    path('<int:pk>/relatorio/', OrderReport, name='order-report'),
     path('relatorio/solicitacoes/', RequestReport, name='request-report'),
]