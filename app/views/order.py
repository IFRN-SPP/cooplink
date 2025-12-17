from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from app.forms import OrderForm, OrderedProductFormSet, OrderedProductForm
from app.models import (
    Call,
    CallProduct,
    Order,
    OrderedProduct,
    Product,
    Institution,
    Cooperative,
)
from app.utils.decorators import (
    staff_required,
    confirm_password,
    order_owner,
    order_evaluated,
)
from app.utils.functions import (
    render_to_pdf,
    get_report_orders,
    calculate_total_products,
    get_week_end,
    get_week_start,
    is_weekend,
    get_report_products,
    calculate_request_product,
)

from ajax.views import AjaxListView, AjaxDeleteView
from ajax.utils import is_ajax


# CRUD Pedidos
class OrderList(LoginRequiredMixin, AjaxListView):
    model = Order
    template_name = "order/list.html"
    partial_list = "partials/order/list.html"
    paginate_by = 6
    object_list = "orders"

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all()
        if not user.is_staff:
            queryset = Order.objects.filter(institution=user.institution)
        return queryset


@login_required
@staff_required
def OrderCreateAdmin(request):
    template_name = "order/create-admin.html"
    context = {}

    if request.method == "GET":
        form = OrderForm()
        form_product = OrderedProductFormSet()

        context["form"] = form
        context["form_product"] = form_product
        return render(request, template_name, context)

    if request.method == "POST":
        form = OrderForm(request.POST)
        form_product = OrderedProductFormSet(request.POST)
        context["form"] = form
        context["form_product"] = form_product

        if form.is_valid() and form_product.is_valid():
            user = request.user
            form.instance.user = user
            order = form.save()
            form_product.instance = order
            form_product.save()

            return redirect("order-list")

        return render(request, template_name, context)


def get_calls(request):
    """
    Returns a list of calls for a specific institution.

    Args:
        request (HttpRequest): The HttpRequest object containing the request data.

    Returns:
        dict: A dictionary containing the calls in the format {'id': call_id, 'text': call_text}.
    """
    data = {}

    if request.method == "GET" and is_ajax(request):
        institution_id = request.GET.get("institution_id")

        if institution_id == "":
            calls = Call.objects.all()
        else:
            instituiton = get_object_or_404(Institution, pk=institution_id)
            calls = instituiton.active_calls

        calls_dict = [
            {"id": call.id, "text": f"Chamada {call.number}"} for call in calls
        ]
        data["calls"] = calls_dict

    else:
        messages.warning(request, "Algum erro aconteceu")
        return redirect("index")

    return JsonResponse(data)


def get_products(request):
    """
    Returns a list of products associated with a specific call.

    Args:
        request (HttpRequest): The HttpRequest object containing the request data.

    Returns:
        dict: A dictionary containing the products in the format {'id': product_id, 'text': product_text}, 'price': product_price}.
    """
    data = {}

    if request.method == "GET" and is_ajax(request):
        call_id = request.GET.get("call_id")
        call = get_object_or_404(Call, pk=call_id)

        call_products = call.products
        products_dict = [
            {"id": call_product.id, "text": str(call_product.product), 'price': str(call_product.price)}
            for call_product in call_products
        ]
        data["products"] = products_dict

    else:
        messages.warning(request, "Algum erro aconteceu")
        return redirect("index")

    return JsonResponse(data)


def get_balance(request):
    """
    Returns the available balance of a specific product.

    Args:
        request (HttpRequest): The HttpRequest object containing the request data.

    Returns:
        str: A string representing the available balance of the product.
    """
    data = {}

    if request.method == "GET" and is_ajax(request):
        product_id = request.GET.get("product_id")

        if product_id == "":
            balance = "Erro: Produto não encontrado"
        else:
            call_product = get_object_or_404(CallProduct, pk=product_id)
            product = get_object_or_404(Product, pk=call_product.product.id)
            balance = f"{call_product.balance} {product.unit}"

        data["balance"] = balance

    else:
        messages.warning(request, "Algum erro aconteceu")
        return redirect("index")

    return JsonResponse(data)


@login_required
def OrderCreate(request):
    template_name = "order/create.html"
    context = {}
    user = request.user

    institution = user.institution
    call = Call.objects.filter(active=True, institution=institution.pk).first()
    context["call"] = call

    if call == None:
        messages.error(
            request, f"{institution} não possui uma Chamada ATIVA para Pedidos."
        )
        return redirect("index")

    today = timezone.now().date()
    if is_weekend(today):
        messages.warning(
            request,
            f"Não é possivel fazer Pedidos hoje. Tente novamente nos proximo dia útil.",
        )
        return redirect("index")

    if request.method == "GET":
        form_product = OrderedProductFormSet()

    if request.method == "POST":
        form_product = OrderedProductFormSet(request.POST)
        if form_product.is_valid():
            order = Order.objects.create(user=user, institution=institution, call=call)
            form_product.instance = order
            form_product.save()

            return redirect("order-list")

    context["form_product"] = form_product
    return render(request, template_name, context)


@login_required
def OrderDetail(request, pk):
    template_name = "order/detail.html"
    context = {}
    user = request.user

    order = get_object_or_404(Order, pk=pk)
    institution = get_object_or_404(Institution, pk=order.call.institution.pk)

    if (not user.is_staff) and (user.institution != institution):
        messages.warning(request, "Você não tem acesso a esse Pedido.")
        return redirect("order-list")

    context["order"] = order
    return render(request, template_name, context)


# Delete de Pedido
class OrderDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Order
    template_name = "partials/order/delete.html"
    success_url = reverse_lazy("order-list")


@login_required
@order_owner
@order_evaluated
def OrderedProductDelete(request, pk):
    template_name = "ordered_product/delete.html"
    context = {}

    ordered_product = get_object_or_404(OrderedProduct, pk=pk)
    context["ordered_product"] = ordered_product

    if request.method == "POST":
        order = ordered_product.order
        ordered_product.delete()

        return redirect("detail-order", pk=order.pk)

    return render(request, template_name, context)


@login_required
@order_owner
@order_evaluated
def OrderedProductUpdate(request, pk):
    template_name = "ordered_product/update.html"
    context = {}

    order = get_object_or_404(Order, pk=pk)

    if request.method == "GET":
        form_product = OrderedProductFormSet(instance=order, queryset=order.products)

        context["order"] = order
        context["form_product"] = form_product

        return render(request, template_name, context)

    if request.method == "POST":
        form = OrderedProductForm(request.POST, instance=order)
        form_product = OrderedProductFormSet(request.POST, instance=order)

        if form_product.is_valid():
            for form in form_product.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            form_product.save()

            return redirect("detail-order", pk=order.pk)

        else:
            context["order"] = order
            context["form"] = form
            context["form_product"] = form_product

            return render(request, template_name, context)


# Avaliar pedido
@login_required
@staff_required
@order_evaluated
def EvaluateOrder(request, pk):
    template_name = "order/evaluate-order.html"
    context = {}
    order = get_object_or_404(Order, pk=pk)

    if request.method == "GET":
        context["order"] = order
        return render(request, template_name, context)

    if request.method == "POST":
        for product in order.products:
            form_status = request.POST.get(f"product_status_{product.pk}")
            print(form_status)
            form_available_quantity = request.POST.get(
                f"product_available_quantity_{product.pk}"
            )

            product.status = form_status
            available_quantity = float(form_available_quantity)
            product_balance = float(product.call_product.balance)

            if available_quantity > product_balance:
                messages.error(
                    request,
                    f"A quantidade disponível de {product.call_product.product} é maior que o seu saldo.",
                )
                return redirect("evaluate-order", pk=order.pk)

            if (product.status == "available") or (product.status == "parcial"):
                product.available_quantity = available_quantity
                product.call_product.balance = (
                    product_balance - product.available_quantity
                )

            product.call_product.save()
            product.save()

        order.status = "approved"
        order.save()

        messages.success(request, f"Pedido avaliado com sucesso!")
        return redirect("detail-order", pk=order.pk)


@login_required
@staff_required
@order_evaluated
def EvaluateOrderDenied(request, pk):
    template_name = "order/denied.html"
    context = {}

    order = get_object_or_404(Order, pk=pk)
    context["order"] = order

    if request.method == "POST":
        for product in order.products:
            product.status = "denied"
            product.save()

        order.status = "denied"
        order.save()
        return redirect("detail-order", pk=order.pk)

    return render(request, template_name, context)


@login_required
@staff_required
@confirm_password
def OrderDelivered(request, pk):
    template_name = "order/delivered.html"
    context = {}

    order = get_object_or_404(Order, pk=pk)
    context["order"] = order

    if request.method == "POST":
        order.status = "delivered"
        order.save()
        return redirect("detail-order", pk=order.pk)

    return render(request, template_name, context)


# Reabrir pedido
@login_required
@staff_required
def ReopenOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if is_ajax(request):
        data = {}

        if request.method == "POST":
            if order.status in ["approved", "denied"]:
                for product in order.products:
                    if product.status in ["available", "parcial"]:
                        product.call_product.balance += product.available_quantity or 0
                        product.call_product.save()

                        product.available_quantity = 0
                        product.status = "pending"
                        product.save()

                order.status = "pending"
                order.save()

                data["form_is_valid"] = True
                data["success_url"] = reverse_lazy("order-list")
                data["message"] = f"Pedido #{order.pk} foi marcado como pendente com sucesso!"
                data["message_class"] = "alert-success"

            else:
                data["form_is_valid"] = False
                data["message"] = "Esse pedido não pode ser reaberto."
                data["message_class"] = "alert-warning"

            return JsonResponse(data)

        context = {"object": order}
        data["html_form"] = render_to_string("partials/order/reopen.html", context, request=request)
        return JsonResponse(data)

    if request.method == "POST":
        if order.status in ["approved", "denied"]:
            for product in order.products:
                if product.status in ["available", "parcial"]:
                    product.call_product.balance += product.available_quantity or 0
                    product.call_product.save()

                    product.available_quantity = 0
                    product.status = "pending"
                    product.save()

            order.status = "pending"
            order.save()

            messages.success(
                request,
                f"Pedido #{order.pk} foi marcado como pendente com sucesso!",
            )
        else:
            messages.warning(request, "Esse pedido não está em um estado que permita reabertura.")

        return redirect("order-list")
    

@login_required
@staff_required
def OrderReport(request, pk):
    template_name = "pdf/order-report.html"
    data = {}
    order = get_object_or_404(Order, pk=pk)

    available_products = order.available_products.order_by('call_product__product__name')
    
    data["order"] = order
    data["available_products"] = available_products
    today = timezone.now().date()
    data["today"] = today

    cooperative = Cooperative.get_instance()
    data["cooperative"] = cooperative
    static_url = request.build_absolute_uri(settings.STATIC_URL)
    data["logo"] = static_url + cooperative.logo

    if request.method == "GET":
        pdf = render_to_pdf(template_name, data)
        return HttpResponse(pdf, content_type="application/pdf")


@login_required
@staff_required
def WeekReport(request):
    template_name = "pdf/week-report.html"
    data = {}

    week_param = request.GET.get('week')
    
    if week_param:
        try:
            reference_date = parse_date(week_param)
            if not reference_date:
                reference_date = timezone.now().date()
        except:
            reference_date = timezone.now().date()
    else:
        reference_date = timezone.now().date()
    
    today = timezone.now().date()
    data["today"] = today
    monday = get_week_start(reference_date)
    data["monday"] = monday
    friday = get_week_end(monday)
    data["friday"] = friday

    orders = get_report_orders(monday, friday)
    
    orders_sorted = sorted(orders, key=lambda order: order.institution.name)
    
    for order in orders_sorted:
        order.available_products_sorted = order.products.filter(
            status__in=['available', 'parcial']
        ).order_by('call_product__product__name')
    
    data["orders"] = orders_sorted
    total_products = calculate_total_products(orders)
    data["total_products"] = total_products

    cooperative = Cooperative.get_instance()
    data["cooperative"] = cooperative
    static_url = request.build_absolute_uri(settings.STATIC_URL)
    data["logo"] = static_url + cooperative.logo

    if request.method == "GET":
        pdf = render_to_pdf(template_name, data)
        return HttpResponse(pdf, content_type="application/pdf")


@login_required
@staff_required
def RequestReport(request):
    template_name = "pdf/request-report.html"
    data = {}

    week_param = request.GET.get('week')
    
    if week_param:
        try:
            reference_date = parse_date(week_param)
            if not reference_date:
                reference_date = timezone.now().date()
        except:
            reference_date = timezone.now().date()
    else:
        reference_date = timezone.now().date()
    
    today = timezone.now().date()
    data["today"] = today
    monday = get_week_start(reference_date)
    data["monday"] = monday
    friday = get_week_end(monday)
    data["friday"] = friday

    orders = get_report_products(monday, friday)
    
    for order in orders:
        if order.status == "pending":
            order.request_products_sorted = order.products.exclude(
                status='denied'
            ).order_by('call_product__product__name')
        else:
            order.request_products_sorted = order.products.filter(
                status__in=['available', 'parcial']
            ).order_by('call_product__product__name')
    
    data["orders"] = orders
    total_requests = calculate_request_product(orders)
    data["total_requests"] = total_requests

    cooperative = Cooperative.get_instance()
    data["cooperative"] = cooperative
    static_url = request.build_absolute_uri(settings.STATIC_URL)
    data["logo"] = static_url + cooperative.logo

    if request.method == "GET":
        pdf = render_to_pdf(template_name, data)
        return HttpResponse(pdf, content_type="application/pdf")


@login_required
@staff_required
def InstitutionReport(request, pk):
    template_name = "pdf/institution-report.html"
    data = {}
    
    week_param = request.GET.get('week')
    
    institution = get_object_or_404(Institution, pk=pk)
    data["institution"] = institution
    
    if week_param:
        try:
            reference_date = parse_date(week_param)
            if not reference_date:
                reference_date = timezone.now().date()
        except:
            reference_date = timezone.now().date()
    else:
        reference_date = timezone.now().date()
    
    today = timezone.now().date()
    data["today"] = today
    monday = get_week_start(reference_date)
    data["monday"] = monday
    friday = get_week_end(monday)
    data["friday"] = friday
    
    data["is_previous_week"] = monday < get_week_start(today)
    data["reference_date"] = reference_date
    
    orders = Order.objects.filter(
        institution=institution,
        timestamp__date__range=[monday, friday]
    ).order_by('timestamp')
    
    data["orders"] = orders
    
    total_products = {}
    total_value = 0
    
    for order in orders:
        for ordered_product in order.products.filter(status__in=['available', 'parcial']):
            product_obj = None
            product_name = "Produto"
            unit = "un"
            price = 0
            
            if hasattr(ordered_product, 'call_product') and ordered_product.call_product:
                if hasattr(ordered_product.call_product, 'product'):
                    product_obj = ordered_product.call_product.product
                    product_name = product_obj.name
                    unit = product_obj.unit
                    price = ordered_product.call_product.price or 0
            
            elif hasattr(ordered_product, 'product') and ordered_product.product:
                product_obj = ordered_product.product
                product_name = product_obj.name
                unit = product_obj.unit
                try:
                    call_product = CallProduct.objects.get(
                        call=order.call,
                        product=product_obj
                    )
                    price = call_product.price or 0
                except CallProduct.DoesNotExist:
                    price = 0
            
            quantity = ordered_product.available_quantity or 0
            
            if product_name not in total_products:
                total_products[product_name] = {
                    'quantity': 0,
                    'unit': unit,
                    'total': 0
                }
            
            total_products[product_name]['quantity'] += quantity
            total_products[product_name]['total'] += quantity * price
            total_value += quantity * price
    
    data["total_products"] = total_products
    data["total_value"] = total_value
    
    cooperative = Cooperative.get_instance()
    data["cooperative"] = cooperative
    static_url = request.build_absolute_uri(settings.STATIC_URL)
    data["logo"] = static_url + cooperative.logo
    
    if request.method == "GET":
        pdf = render_to_pdf(template_name, data)
        return HttpResponse(pdf, content_type="application/pdf")


@login_required
@staff_required
def ReportHistory(request):
    template_name = "order/report-history.html"
    context = {}
    
    page = request.GET.get('page', 1)
    
    today = timezone.now().date()
    current_monday = get_week_start(today)
    
    all_weeks = []
    for i in range(0, 52):
        week_date = current_monday - timedelta(weeks=i)
        week_monday = get_week_start(week_date)
        week_friday = get_week_end(week_monday)
        all_weeks.append({
            'monday': week_monday,
            'friday': week_friday,
            'label': f"Semana {week_monday.strftime('%d/%m')} - {week_friday.strftime('%d/%m/%Y')}",
            'value': week_monday.strftime('%Y-%m-%d')
        })
    
    weeks_with_orders = []
    
    for week in all_weeks:
        has_orders = Order.objects.filter(
            timestamp__date__range=[week['monday'], week['friday']]
        ).exists()
        
        if has_orders:
            weeks_with_orders.append(week)
        elif week['monday'] == current_monday:
            weeks_with_orders.append(week)
    
    paginate_by = 6
    paginator = Paginator(weeks_with_orders, paginate_by)
    
    try:
        weeks_page = paginator.page(page)
    except PageNotAnInteger:
        weeks_page = paginator.page(1)
    except EmptyPage:
        weeks_page = paginator.page(paginator.num_pages)
    
    context['weeks'] = weeks_page.object_list
    context['page'] = weeks_page
    context['institutions'] = Institution.objects.all().order_by('name')
    context['current_week'] = current_monday
    
    if is_ajax(request) and request.GET.get('table_only') == 'true':
        template_name = "order/report-history.html"
    
    return render(request, template_name, context)
