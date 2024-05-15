from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.utils.decorators import staff_required
from app.models import Order, Call, CallProduct


@login_required
def index(request):
    template_name = 'index.html'
    context = {}
    user = request.user

    if user.is_staff:
        return redirect('index-admin')

    orders = Order.objects.filter(institution=user.institution)[:5]
    call= Call.objects.filter(active=True, institution=user.institution).first()
    products = CallProduct.objects.filter(call=call)

    context['orders'] = orders
    context['call'] = call
    context['products'] = products
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

