from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import constants
from django.contrib import messages

from app.forms import CallForm, CallProductFormSet
from app.models import Call, CallProduct, Institution
from app.utils.decorators import staff_required
from app.utils.mixins import StaffRequiredMixin

from django.views.generic.edit import UpdateView, DeleteView

#CRUD CHAMADA
@login_required
def CallList(request):
    template_name = 'call/list.html'
    context = {}
    user = request.user

    calls = Call.objects.all()
    if not user.is_staff:
        calls = Call.objects.filter(institution=user.institution)

    context['calls'] = calls
    return render(request, template_name, context)


class CallUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Call
    fields = ['number', 'institution', 'start','end']
    template_name = 'call/create.html'
    success_url = reverse_lazy('call-list')


class CallDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model= Call
    template_name = 'call/delete.html'
    success_url = reverse_lazy('call-list')


@login_required
@staff_required
def CallCreate(request):
    template_name = 'call/create.html'
    context = {}

    if request.method == 'GET':
        form = CallForm()
        form_product = CallProductFormSet()
    
    if request.method == 'POST':
        form = CallForm(request.POST)
        form_product = CallProductFormSet(request.POST)
        if form.is_valid() and form_product.is_valid(): 
            call = form.save() 
            form_product.instance = call 
            form_product.save()
            messages.add_message(request, constants.SUCCESS, f"{form.instance} foi cadastrada com sucesso!")
            return redirect('call-list') 
            
    context['form'] = form
    context['form_product'] = form_product
    return render(request, template_name, context)
        

@login_required
@staff_required
def CallProductUpdate(request, pk):
    template_name = 'call-product/update.html'
    context = {}

    call = get_object_or_404(Call, pk=pk)
    context['call'] = call

    if request.method == 'GET':
        products = CallProduct.objects.filter(call=call)
        form_product = CallProductFormSet(instance=call, queryset=products)    
        context['form_product'] = form_product

    if request.method == 'POST':
        form_product = CallProductFormSet(request.POST, instance=call)

        if form_product.is_valid():
            for form in form_product.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            form_product.save()
            messages.add_message(request, constants.SUCCESS, f"Produtos da {call} foram atualizados com sucesso!")
            return redirect('detail-call', pk=call.pk) 

    context['form_product'] = form_product
    return render(request, template_name, context)


@login_required
def CallDetail(request, pk):
    template_name = 'call/detail.html'
    context = {}
    user = request.user

    call = get_object_or_404(Call, pk=pk)
    products = CallProduct.objects.filter(call=call)
    institution = get_object_or_404(Institution, pk=call.institution.pk)

    if (not user.is_staff) and (institution != user.institution):
        messages.add_message(request, constants.WARNING, "Você não tem acesso a essa página.")
        return redirect('index')
    
    context['call'] = call
    context['products'] = products
    return render(request, template_name, context)


@login_required
@staff_required
def CallProductDelete(request, pk):
    template_name = 'call-product/delete.html'
    context = {}
    
    call_product = get_object_or_404(CallProduct, pk=pk)
    context['call_product'] = call_product
    
    if request.method == 'POST':
        call_product.delete()
        return redirect('detail-call', pk=call_product.call.pk)

    return render(request, template_name, context)
