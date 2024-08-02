from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from app.forms import ProductForm
from app.models import Product
from ajax.views import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from app.utils.mixins import StaffRequiredMixin


# CRUD PRODUTOS
class ProductList(LoginRequiredMixin, StaffRequiredMixin, AjaxListView):
    model = Product
    template_name = 'product/list.html'
    partial_list = 'partials/product/list.html'
    paginate_by = 7

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get('search', '')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context(self):
        context = {}
        name = self.request.GET.get('search', '')
        context['name'] = name
        if self.paginate_by:
            context['filter'] = f'&search={name}'
        return context


class ProductCreate(AjaxCreateView):
    form_class = ProductForm
    template_name = 'partials/product/create.html'
    success_url = reverse_lazy('product-list')
    message = "Produto adicionado com sucesso!"
    message_class = "alert-success"


class ProductUpdate(AjaxUpdateView):
    form_class = ProductForm
    template_name = 'partials/product/update.html'
    success_url = reverse_lazy('product-list')
    message = "Produto atualizado com sucesso!"
    message_class = "alert-success"


class ProductDelete(AjaxDeleteView):
    model = Product
    template_name = 'partials/product/delete.html'
    success_url = reverse_lazy('product-list')
    message = "Produto deletado com sucesso!"
    message_class = "alert-primary"