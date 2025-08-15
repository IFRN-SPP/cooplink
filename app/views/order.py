from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

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
        dict: A dictionary containing the products in the format {'id': product_id, 'text': product_text}.
    """
    data = {}

    if request.method == "GET" and is_ajax(request):
        call_id = request.GET.get("call_id")
        call = get_object_or_404(Call, pk=call_id)

        call_products = call.products
        products_dict = [
            {"id": call_product.id, "text": str(call_product.product)}
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

    if (order.status != "approved") and (order.status != "delivered"):
        messages.warning(
            request,
            "Não é possível gerar o relatório de um Pedido que não foi aprovado ou entregue",
        )
        return redirect("detail-order", pk)

    data["order"] = order
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

    today = timezone.now().date()
    data["today"] = today
    monday = get_week_start(today)
    data["monday"] = monday
    friday = get_week_end(monday)
    data["friday"] = friday

    orders = get_report_orders(monday, friday)
    data["orders"] = orders
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

    today = timezone.now().date()
    data["today"] = today
    monday = get_week_start(today)
    data["monday"] = monday
    friday = get_week_end(monday)
    data["friday"] = friday

    orders = get_report_products(monday, friday)
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
