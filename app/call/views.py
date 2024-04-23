from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import  CallProductForm, CallForm, CallProductFormSet
from ..models import Call, CallProduct

from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView

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

