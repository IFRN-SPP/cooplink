from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .ajax import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from .registration import ConfirmPasswordMixin
from .forms import InstitutionForm, ProductForm, UserCreateForm, UserUpdateForm, SetPasswordForm, PermissionForm, CallProductForm, CallForm, CallProductFormSet, OrderForm, OrderedProductFormSet
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

class CallUpdate(LoginRequiredMixin, UpdateView):
    model = Call
    fields = ['number', 'institution', 'start','end', 'active']
    template_name = 'call/create.html'
    success_url = reverse_lazy('call-list')

class CallDelete(LoginRequiredMixin, DeleteView):
    model= Call
    template_name = 'call/delete.html'
    success_url = reverse_lazy('call-list')

# CRUD Chamada Function Based Views


@login_required
def CallCreate(request):
    # se o metodo for GET (deseja adcionar um produto)
    if request.method == 'GET':
        form = CallForm() # form de chamada
        form_product_factory = CallProductFormSet
        form_product = form_product_factory() # form de produtos
        context = {
            'form':form, 
            'form_product': form_product
        } # dou o contexto
        return render(request, 'call/create.html', context) # passo o html do form
    
    # se for POST (deseja enviar dado produto)
    if request.method == 'POST':
        form = CallForm(request.POST) # post form de chamada
        form_product_factory = CallProductFormSet
        form_product = form_product_factory(request.POST)

        if form.is_valid() and form_product.is_valid(): 
            call = form.save() # salva chamada 
            form_product.instance = call # relaciona os produtos a chamada salva
            form_product.save()
            
            return redirect('call-list') # redireciono
        else:
            context = {
                'form': form,
                'form_product': form_product,
            }
            return render(request, 'call/create.html', context)
        

@login_required
def CallProductUpdate(request, pk):
    # pego a pk da call, na qual quero editar os produtos
    call = get_object_or_404(Call, pk=pk)

    if request.method == 'GET':
        # obtém todos os produtos relacionados à chamada
        products = CallProduct.objects.filter(call=call)
        form_product_factory = CallProductFormSet
        form_product = form_product_factory(instance=call, queryset=products)
        context = {
            'call': call,
            'form_product': form_product,
        }
        return render(request, 'call-product/update.html', context)

    # Se o método for POST, processa os dados submetidos
    if request.method == 'POST':
        form = CallProductForm(request.POST, instance=call)
        form_product_factory = CallProductFormSet 
        form_product = form_product_factory(request.POST, instance=call)

        if form_product.is_valid():
            # deleta os produtos que foram excluidos
            for form in form_product.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            form_product.save()
            return redirect('detail-call', pk=call.pk)  # Redireciona para a página da chamada
        else:
            context = {
                'call': call,
                'form': form,
                'form_product': form_product,
            }
            return render(request, 'call-product/update.html', context)


@login_required
def CallDetail(request, pk):
    call = get_object_or_404(Call, pk=pk)
    products = CallProduct.objects.filter(call=call)
    context = {
        'call': call, 
        'products': products,
    }
    return render(request, 'call/detail.html', context)


@login_required
def CallProductDelete(request, pk):
    call_product = get_object_or_404(CallProduct, pk=pk)
    if request.method == 'POST':
        call_product.delete()
        return redirect('detail-call', pk=call_product.call.pk) # retorna para a página da chamada
    return render(request, 'call-product/delete.html', {'call_product': call_product})


# CRUD Pedidos

@login_required
def OrderList(request):
    order = Order.objects.all()
    context = {'order_list': order}
    return render(request, 'order/list.html', context)

@login_required
def OrderCreate(request):
    if request.method == 'GET':
        form = OrderForm()
        form_product_factory = OrderedProductFormSet
        form_product = form_product_factory()
        context = {
            'form':form, 
            'form_product': form_product
        } 
        
        return render(request, 'order/create.html', context)
    

    if request.method == 'POST':
        form = OrderForm(request.POST) 
        form_product_factory = OrderedProductFormSet
        form_product = form_product_factory(request.POST)

        if form.is_valid() and form_product.is_valid():
            order = form.save()
            form.save() 
            form_product.instance = order 
            form_product.save()
            
            return redirect('order-list') 
        else:
            context = {
                'form': form,
                'form_product': form_product,
            }
            return render(request, 'order/create.html', context)
        
@login_required
def OrderDetail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    products = OrderedProduct.objects.filter(order=order)
    context = {
        'order': order, 
        'products': products,
    }
    return render(request, 'order/detail.html', context)

# deleta os pedidos, não os produtos dos pedidos em especifico
def OrderDelete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order-list') 
    return render(request, 'order/delete.html', {'order': order})



