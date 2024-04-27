from django.views.generic.edit import UpdateView
from app.forms import ConfirmPasswordForm

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
