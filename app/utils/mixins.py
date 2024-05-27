import datetime
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .views import ConfirmPasswordView


class ConfirmPasswordMixin(LoginRequiredMixin, View):
    """
    Mixin to check if the user is logged in and prompt for password confirmation
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch method to prompt for password confirmation.
        """
        if request.user.is_authenticated:
            last_login = request.user.last_login
            timespan = last_login + datetime.timedelta(seconds=60)
            if timezone.now() > timespan:
                return ConfirmPasswordView.as_view()(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin:
    """
    Mixin to check if the user is a staff member
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.warning(request, "Você não tem acesso a essa página.")
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
