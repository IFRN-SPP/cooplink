from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .ajax import *
from .models import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

# CRUD INSTITUIÇÃO
class InstitutionList(LoginRequiredMixin, JsonListView):
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
class ProductList(LoginRequiredMixin, JsonListView):
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
class UserList(LoginRequiredMixin, JsonListView):
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


#CRUD CHAMADA

class CallList(LoginRequiredMixin, ListView):
    model= Call
    template_name = 'call/list.html'

class CallCreate(LoginRequiredMixin, CreateView):
    model = Call
    fields = ['number', 'institution', 'start','end', 'active']
    template_name = 'call/create.html'
    success_url = reverse_lazy('call-list')

class CallUpdate(LoginRequiredMixin, UpdateView):
    model = Call
    fields = ['number', 'institution', 'start','end', 'active']
    template_name = 'call/create.html'
    success_url = reverse_lazy('call-list')

class CallDelete(LoginRequiredMixin, DeleteView):
    model= Call
    template_name = 'call/delete.html'
    success_url = reverse_lazy('call-list')
