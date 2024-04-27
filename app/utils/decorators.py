import datetime
from functools import wraps

from django.utils import timezone
from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .views import ConfirmPasswordView
from app.models import Order, Institution

# Crie seus decorators aqui
def confirm_password(func):
    """
    Decorator for check if the user is logged in and prompt for password confirmation
    """
    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        last_login = request.user.last_login
        timespan = last_login + datetime.timedelta(seconds=60)
        if timezone.now() > timespan:
            return ConfirmPasswordView.as_view()(request, *args, **kwargs)
        return func(request, *args, **kwargs)
    return _wrapped_view

def staff_required(func):
    """
    Decorator for check if the request user is a staff member 
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.add_message(request, constants.WARNING, "Você não tem acesso a essa página.")    
            return redirect('index')  
        return func(request, *args, **kwargs)
    return _wrapped_view

def order_owner(func):
    """
    Decorator to check if the request user is part of the order institution
    """
    def _wrapped_view(request, pk, *args, **kwargs): 
        user = request.user
        order = get_object_or_404(Order, pk=pk)
        institution = get_object_or_404(Institution, pk=order.call.institution.pk)

        if (user != order.user) and (user.institution != institution):
            messages.add_message(request, constants.WARNING, "Você não tem acesso a esse Pedido.")
            return redirect('order-list')

        return func(request, pk, *args, **kwargs)
    return _wrapped_view

def order_evaluated(func):
    """
    Decorator to prevent updates to orders already evaluated
    """
    def _wrapped_view(request, pk, *args, **kwargs): 
        order = get_object_or_404(Order, pk=pk)
        if order.status != 'pending':
            messages.add_message(request, constants.WARNING, 'Você não pode alterar um Pedido que não está "Pendente".')
            return redirect('order-list')
        
        return func(request, pk, *args, **kwargs)
    return _wrapped_view