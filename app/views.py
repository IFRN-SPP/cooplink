from django.shortcuts import render
from .ajax import *
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

# CRUD INSTITUIÇÃO
class InstitutionList(JsonListView):
    template_name = 'institution/list.html'
    partial_list = 'partials/institution/list.html'
    model = Institution
        
class InstitutionCreate(JsonCreateView, InstitutionList):
    template_name = 'partials/institution/create.html'
    form_class = InstitutionForm

class InstitutionUpdate(JsonUpdateView, InstitutionList):
    template_name = 'partials/institution/update.html'
    form_class = InstitutionForm

class InstitutionDelete(JsonDeleteView, InstitutionList):
    template_name = 'partials/institution/delete.html'

# CRUD PRODUTOS
class ProductList(JsonListView):
    template_name = 'product/list.html'
    partial_list = 'partials/product/list.html'
    model = Product

class ProductCreate(JsonCreateView, ProductList):
    template_name = 'partials/product/create.html'
    form_class = ProductForm

class ProductUpdate(JsonUpdateView, ProductList):
    template_name = 'partials/product/update.html'
    form_class = ProductForm

class ProductDelete(JsonDeleteView, ProductList):
    template_name = 'partials/product/delete.html'