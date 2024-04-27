from django.urls import path
from app.views.product import ProductList, ProductCreate, ProductUpdate, ProductDelete

# Adicione suas URLs aqui
urlpatterns = [
    path("", ProductList.as_view(), name="product-list"),
    path("js/create/", ProductCreate.as_view(), name="js-create-product"),
    path("js/update/<int:pk>/", ProductUpdate.as_view(), name="js-update-product"),
    path("js/delete/<int:pk>/", ProductDelete.as_view(), name="js-delete-product"),
]