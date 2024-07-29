from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from app.forms import InstitutionForm
from app.models import Institution, UserProfile
from app.utils.mixins import StaffRequiredMixin

from ajax.views import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView


# CRUD INSTITUIÇÃO
class InstitutionList(LoginRequiredMixin, StaffRequiredMixin, AjaxListView):
    model = Institution
    template_name = 'institution/list.html'
    partial_list = 'partials/institution/list.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = Institution.objects.all()
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


class InstitutionCreate(AjaxCreateView):
    form_class = InstitutionForm
    template_name = 'partials/institution/create.html'
    success_url = reverse_lazy('institution-list')
    message = "Instituição cadastrada com sucesso!"
    message_class = "alert-success"


class InstitutionUpdate(AjaxUpdateView):
    form_class = InstitutionForm
    template_name = 'partials/institution/update.html'
    success_url = reverse_lazy('institution-list')
    message = "Instituição atualizado com sucesso!"
    message_class = "alert-success"


class InstitutionDelete(AjaxDeleteView):
    model = Institution
    template_name = 'partials/institution/delete.html'
    success_url = reverse_lazy('institution-list')
    message = "Instituição deletado com sucesso!"
    message_class = "alert-primary"

@login_required
def InstitutionDetail(request, pk):
    template_name = 'institution/detail.html'
    context = {}
    user = request.user
    institution = get_object_or_404(Institution, pk=pk)

    if (not user.is_staff) and (user.institution != institution):
        messages.warning(request, "Você não tem acesso a essa Instituição.")
        return redirect('institution-list')
    
    context['institution'] = institution
    return render(request, template_name, context)

