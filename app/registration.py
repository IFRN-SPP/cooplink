from django.utils import timezone
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ConfirmPasswordForm

from django.views import View
from django.views.generic.edit import UpdateView

# View de confirmação de Senha
class ConfirmPasswordView(UpdateView):
    """
    View for confirm passwoard.
    """
    form_class = ConfirmPasswordForm
    template_name = 'registration/confirm-password.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()
    
# Mixin de Ccnfirmação de senha
class ConfirmPasswordMixin(LoginRequiredMixin, View):
    """
    Mixin to check if the user is logged in and prompt for password confirmation
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch method to prompt for password confirmation.
        """
        if request.user.is_authenticated:
        # -> Método com last_login
            last_login = request.user.last_login
            timespan = last_login + datetime.timedelta(seconds=60)
            if timezone.now() > timespan:
                return ConfirmPasswordView.as_view()(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
