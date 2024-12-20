from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.contrib.auth.forms import SetPasswordForm
from django.views.generic.edit import UpdateView, FormView, CreateView

from app.forms import UserCreateForm, UserUpdateForm, PermissionForm, UserActiveForm
from app.models import UserProfile
from app.utils.mixins import ConfirmPasswordMixin, StaffRequiredMixin

from ajax.views import AjaxListView, AjaxUpdateView, AjaxDeleteView


# CRUD USUARIO
class UserList(LoginRequiredMixin, StaffRequiredMixin, AjaxListView):
    model = UserProfile
    template_name = 'user/list.html'
    partial_list = 'partials/user/list.html'
    paginate_by = 6


class UserCreate(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        messages.success(self.request, f'O usuário {form.instance} foi cadastrado com sucesso!')
        return super().form_valid(form)


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
        form.save()
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


class UserUpdateActive(StaffRequiredMixin, ConfirmPasswordMixin, UpdateView):
    model = UserProfile
    form_class = UserActiveForm
    template_name = 'user/change-active.html'
    success_url = reverse_lazy('user-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['is_active'] = True
        if self.object.is_active:
            initial['is_active'] = False
        return initial

    def form_valid(self, form):
        if form.instance.is_active == True:
            messages.success(self.request, f'{form.instance.first_name} {form.instance.last_name} foi ativado com sucesso!')
        if form.instance.is_active == False:
            messages.success(self.request, f'{form.instance.first_name} {form.instance.last_name} foi desativado com sucesso!')
        return super().form_valid(form)


class UserDelete(AjaxDeleteView):
    model = UserProfile
    template_name =  'partials/user/delete.html'
    success_url = reverse_lazy('user-list')
    message = "Usuário deletado com sucesso!"
    message_class = "alert-primary"

