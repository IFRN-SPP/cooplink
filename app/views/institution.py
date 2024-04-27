from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from app.forms import InstitutionForm
from app.models import Institution
from app.utils.ajax import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView 
from app.utils.mixins import StaffRequiredMixin

# CRUD INSTITUIÇÃO
class InstitutionList(LoginRequiredMixin, StaffRequiredMixin, AjaxListView):
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
