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

# CRUD USUARIO
class UserList(JsonListView):
    template_name = 'user/list.html'
    partial_list = 'partials/user/list.html'
    model = UserProfile

class UserCreate(JsonCreateView, UserList):
    template_name = 'partials/user/create.html'
    form_class = UserCreateForm

class UserUpdate(JsonUpdateView, UserList):
    template_name =  'partials/user/update.html'
    form_class = UserUpdateForm

class UserDelete(JsonDeleteView, UserList):
    template_name =  'partials/user/delete.html'