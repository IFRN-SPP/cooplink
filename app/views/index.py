from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.utils.decorators import staff_required
from app.utils.functions import render_to_pdf, get_relatory_orders, calculate_total_products, get_week_end, get_week_start
from app.models import Order, Call, CallProduct

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


@login_required
@staff_required
def week_relatory(request):
    template_name = 'pdf/week-relatory.html'
    data = {}

    today = timezone.now().date()
    data['today'] = today
    monday = get_week_start(today)
    data['monday'] = monday
    friday = get_week_end(monday)
    data['friday'] = friday

    orders = get_relatory_orders(monday, friday)
    data['orders'] = orders
    total_products = calculate_total_products(orders)
    data['total_products'] = total_products 
    
    if request.method == 'GET':
        pdf = render_to_pdf(template_name, data)
        return HttpResponse(pdf, content_type='application/pdf')

