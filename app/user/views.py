from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.forms import SetPasswordForm
from ..forms import UserCreateForm, UserUpdateForm, PermissionForm
from ..models import UserProfile
from ..utils.ajax import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from ..utils.mixins import ConfirmPasswordMixin

from django.views.generic.edit import UpdateView, FormView

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
