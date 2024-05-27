from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.forms import SetPasswordForm
from django.views.generic.edit import UpdateView, FormView

from app.forms import UserCreateForm, UserUpdateForm, PermissionForm
from app.models import UserProfile
from app.utils.mixins import ConfirmPasswordMixin, StaffRequiredMixin

from ajax.views import AjaxListView, AjaxCreateView, AjaxUpdateView, AjaxDeleteView


# CRUD USUARIO
class UserList(LoginRequiredMixin, StaffRequiredMixin, AjaxListView):
    model = UserProfile
    template_name = 'user/list.html'
    partial_list = 'partials/user/list.html'
    paginate_by = 6


class UserCreate(AjaxCreateView):
    form_class = UserCreateForm
    template_name = 'partials/user/create.html'
    success_url = reverse_lazy('user-list')
    message = "Usuário ADICIONADO com sucesso!"
    message_class = "alert-success"


class UserUpdate(AjaxUpdateView):
    form_class = UserUpdateForm
    template_name =  'partials/user/update.html'
    success_url = reverse_lazy('user-list')
    message = "Usuário ATUALIZADO com sucesso!"
    message_class = "alert-success"


class UserUpdatePassword(StaffRequiredMixin, ConfirmPasswordMixin, FormView):
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


class UserUpdatePermission(StaffRequiredMixin, ConfirmPasswordMixin, UpdateView):
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
    message = "Usuário DELETADO com sucesso!"
    message_class = "alert-primary"

