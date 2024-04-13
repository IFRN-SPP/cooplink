from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .ajax import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from .registration import ConfirmPasswordMixin
from .forms import InstitutionForm, ProductForm, UserCreateForm, UserUpdateForm, SetPasswordForm, PermissionForm, CallProductForm, CallForm
from .models import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

# CRUD INSTITUIÇÃO
class InstitutionList(LoginRequiredMixin, AjaxListView):
    model = Institution
    template_name = 'institution/list.html'
    partial_list = 'partials/institution/list.html'
        
class InstitutionCreate(AjaxCreateView):
    form_class = InstitutionForm
    template_name = 'partials/institution/create.html'
    success_url = reverse_lazy('institution-list')

class InstitutionUpdate(AjaxUpdateView):
    form_class = InstitutionForm
    template_name = 'partials/institution/update.html'
    success_url = reverse_lazy('institution-list')

class InstitutionDelete(AjaxDeleteView):
    model = Institution
    template_name = 'partials/institution/delete.html'
    success_url = reverse_lazy('institution-list')

# CRUD PRODUTOS
class ProductList(LoginRequiredMixin, AjaxListView):
    model = Product
    template_name = 'product/list.html'
    partial_list = 'partials/product/list.html'

class ProductCreate(AjaxCreateView):
    form_class = ProductForm
    template_name = 'partials/product/create.html'
    success_url = reverse_lazy('product-list')

class ProductUpdate(AjaxUpdateView):
    form_class = ProductForm
    template_name = 'partials/product/update.html'
    success_url = reverse_lazy('product-list')

class ProductDelete(AjaxDeleteView):
    model = Product
    template_name = 'partials/product/delete.html'
    success_url = reverse_lazy('product-list')

# CRUD USUARIO
class UserList(LoginRequiredMixin, AjaxListView):
    model = UserProfile
    template_name = 'user/list.html'
    partial_list = 'partials/user/list.html'

class UserCreate(AjaxCreateView):
    form_class = UserCreateForm
    template_name = 'partials/user/create.html'
    success_url = reverse_lazy('user-list')

class UserUpdate(AjaxUpdateView):
    form_class = UserUpdateForm
    template_name =  'partials/user/update.html'
    success_url = reverse_lazy('user-list')

# View para Admin mudar senha do usuário
class UserUpdatePassword(ConfirmPasswordMixin, FormView):
    form_class = SetPasswordForm
    template_name = 'user/change-password.html'
    success_url = reverse_lazy('user-list') 

    def form_valid(self, form):
        pk = self.kwargs['pk']
        user = UserProfile.objects.get(pk=pk)
        messages.success(self.request, f'A senha de {user} foi alterada com sucesso!')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs['pk']
        user = UserProfile.objects.get(pk=pk)
        kwargs['user'] = user
        return kwargs

# View para Admin mudar permissão do usuário
class UserUpdatePermission(ConfirmPasswordMixin, UpdateView):
    model = UserProfile
    form_class = PermissionForm
    template_name = 'user/change-permission.html'
    success_url = reverse_lazy('user-list')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['is_staff'] = True   
        if self.object.is_staff:
            initial['is_staff'] = False  
        return initial

    def form_valid(self, form):
        messages.success(self.request, f'A permissão de {form.instance} foi alterada com sucesso!')
        return super().form_valid(form)

class UserDelete(AjaxDeleteView):
    model = UserProfile
    template_name =  'partials/user/delete.html'
    success_url = reverse_lazy('user-list')


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

# CRUD Produtos da Chamada

@login_required
def CallProductList(request):
    call_products = CallProduct.objects.all()
    context = {'call_product_list': call_products}
    return render(request, 'call-product/list.html', context)

@login_required
def CallProductCreate(request):
    # se o metodo for GET (deseja adcionar um produto)
    if (request.method == 'GET'):
        form = CallProductForm() # trago o form 

        form_product_factory = inlineformset_factory(Call, CallProduct, form= CallProductForm, extra=2) 
        form_product= form_product_factory()
        context = {
            'form':form, 
            'form_product': form_product
        } # dou o contexto

        return render(request, 'call-product/create.html', context) # passo o html do form
    
    # se for POST (deseja enviar dado produto)
    elif (request.method == 'POST'):
        form = CallProductForm(request.POST)
        form_product_factory = inlineformset_factory(Call, CallProduct, form= CallProductForm)
        form_product= form_product_factory(request.POST)

        if form.is_valid() and form_product.is_valid():
            call_product_instance = form.save(commit=False)  # não salva de imediato no formulário no callproductform até ter uma logica concluida
            call_instance = Call.objects.first()   # obtém ou cria uma instância/pk/obj no modelo Call 

            call_product_instance.call = call_instance
            call_product_instance.save()

            # salva o formulário de conjunto em linha (inlineformset)
            form_product.instance = call_product_instance
            form_product.instance.save()
            return redirect('call-product-list') # redireciono
        else:
            form = CallProductForm()
            form_product_factory = inlineformset_factory(Call, CallProduct, form=CallProductForm, extra=2)
            form_product = form_product_factory()

            context = {
                'form': form,
                'form_product': form_product,
            }
            return render(request, 'call-product/create.html', context)

@login_required
def CallProductDelete(request, pk):
    call_product = get_object_or_404(CallProduct, pk=pk)
    if (request.method == 'POST'):
        call_product.delete()
        return redirect('call-product-list')
    return render(request, 'call-product/delete.html', {'call_product': call_product})

