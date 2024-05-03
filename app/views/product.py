from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from app.forms import ProductForm
from app.models import Product
from ajax.views import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView 
from app.utils.mixins import StaffRequiredMixin

from django.contrib.messages import constants

# CRUD PRODUTOS
class ProductList(LoginRequiredMixin, StaffRequiredMixin, AjaxListView):
    model = Product
    template_name = 'product/list.html'
    partial_list = 'partials/product/list.html'
    paginate_by = 6

class ProductCreate(AjaxCreateView):
    form_class = ProductForm
    template_name = 'partials/product/create.html'
    success_url = reverse_lazy('product-list')
    message = "Produto ADICIONADO com sucesso!"
    message_class = "alert-success"

class ProductUpdate(AjaxUpdateView):
    form_class = ProductForm
    template_name = 'partials/product/update.html'
    success_url = reverse_lazy('product-list')
    message = "Produto ATUALIZADO com sucesso!"
    message_class = "alert-success"

class ProductDelete(AjaxDeleteView):
    model = Product
    template_name = 'partials/product/delete.html'
    success_url = reverse_lazy('product-list')
    message = "Produto DELETADO com sucesso!"
    message_class = "alert-primary"