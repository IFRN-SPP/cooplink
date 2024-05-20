from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from ajax.views import AjaxListView, AjaxDeleteView
from app.forms import CallForm, CallProductFormSet, CallActiveForm
from app.models import Call, CallProduct, Institution
from app.utils.decorators import staff_required
from app.utils.mixins import StaffRequiredMixin

from django.views.generic.edit import UpdateView


class CallList(LoginRequiredMixin, AjaxListView):
    model = Call
    template_name = 'call/list.html'
    partial_list = 'partials/call/list.html'
    paginate_by = 6
    object_list = 'calls'

    def get_queryset(self):
        user = self.request.user
        queryset = Call.objects.all()
        if not user.is_staff:
            queryset = Call.objects.filter(institution=user.institution)

        number = self.request.GET.get('search', '')
        if number:
            queryset = queryset.filter(number__icontains=number)
        return queryset

    def get_context(self):
        context = {}
        number = self.request.GET.get('search', '')
        context['number'] = number
        if self.paginate_by:
            context['filter'] = f'&search={number}'
        return context


class CallUpdate(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Call
    fields = ['number', 'institution', 'start', 'end']
    template_name = 'call/create.html'
    success_url = reverse_lazy('call-list')


@login_required
@staff_required
def CallUpdateActive(request, pk):
    template_name = 'call/change-active.html'
    context = {}
    call = get_object_or_404(Call, pk=pk)
    context['call'] = call

    if request.method == 'GET':
        initial = {'active': not call.active}
        form = CallActiveForm(initial=initial)

    if request.method == 'POST':
        form = CallActiveForm(request.POST, instance=call)
        if form.is_valid():
            form.save()
            if form.cleaned_data['active']:
                messages.success(request, f'A {call} agora está ATIVA!')
            else:
                messages.warning(request, f'A {call} agora está INATIVA!')
            return redirect('call-list')

        if form.errors:
            messages.warning(request, f'Existe outra Chamada ATIVA de {call.institution}! Desative a outra chamada antes de ativar a {call}')
            return redirect('call-list')

    context['form'] = form
    return render(request, template_name, context)


class CallDelete(LoginRequiredMixin, StaffRequiredMixin, AjaxDeleteView):
    model= Call
    template_name = 'partials/call/delete.html'
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
            messages.success(request, f"{form.instance} foi cadastrada com sucesso!")
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
        form_product = CallProductFormSet(instance=call, queryset=call.products)
        context['form_product'] = form_product

    if request.method == 'POST':
        form_product = CallProductFormSet(request.POST, instance=call)

        if form_product.is_valid():
            for form in form_product.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            form_product.save()
            messages.success(request, f"Produtos da {call} foram atualizados com sucesso!")
            return redirect('detail-call', pk=call.pk)

    context['form_product'] = form_product
    return render(request, template_name, context)


@login_required
def CallDetail(request, pk):
    template_name = 'call/detail.html'
    context = {}
    user = request.user

    call = get_object_or_404(Call, pk=pk)
    institution = get_object_or_404(Institution, pk=call.institution.pk)

    if (not user.is_staff) and (institution != user.institution):
        messages.warning(request, "Você não tem acesso a essa página.")
        return redirect('index')

    context['call'] = call
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

