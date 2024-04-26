from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .utils.decorators import staff_required
from .models import Order, Call, CallProduct

# Create your views here.
@login_required
def index(request):
    template_name = 'index.html'
    context = {}
    user = request.user

    if user.is_staff:
        return redirect('index-admin')

    orders = Order.objects.filter(institution=user.institution)
    call= Call.objects.filter(active=True, institution=user.institution).first()
    products = CallProduct.objects.filter(call=call)

    context['call'] = call
    context['products'] = products
    context['orders'] = orders
    return render(request, template_name, context)

@login_required
@staff_required
def index_admin(request):
    template_name = 'index-admin.html'
    context = {}

    calls = Call.objects.filter(active=True)
    orders = Order.objects.filter(status='pending')

    context['calls'] = calls
    context['orders'] = orders
    return render(request, template_name, context)
