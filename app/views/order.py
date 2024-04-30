from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from app.forms import OrderForm, OrderedProductFormSet, OrderedProductForm
from app.models import Call, CallProduct, Order, OrderedProduct, Product, Institution
from app.utils.decorators import staff_required, confirm_password, order_owner, order_evaluated

from django.contrib.messages import constants
from django.contrib import messages

# CRUD Pedidos

@login_required
def OrderList(request):
    template_name =  'order/list.html'
    context = {}
    user = request.user

    order = Order.objects.all()
    if not user.is_staff:
        order = Order.objects.filter(institution=user.institution)

    context['order_list'] = order
    return render(request, template_name, context)

# Create para Admin
@login_required
@staff_required
def OrderCreateAdmin(request):
    template_name = 'order/create-admin.html'
    context = {}

    if request.method == 'GET':
        form = OrderForm()
        form_product = OrderedProductFormSet()
        
        context['form'] = form 
        context['form_product'] = form_product
        return render(request, template_name, context)

    if request.method == 'POST':
        form = OrderForm(request.POST) 
        form_product = OrderedProductFormSet(request.POST)
        context['form'] = form 
        context['form_product'] = form_product

        if form.is_valid() and form_product.is_valid():
            user = request.user
            form.instance.user = user
            order = form.save()
            form_product.instance = order 
            form_product.save()
            
            return redirect('order-list') 
        
        return render(request, template_name, context)       

# função para atualizar dinamicamente o select de call no form   
def get_calls(request):
    data = {}

    if request.method == 'GET':
        institution_id = request.GET.get('institution_id')

        if institution_id == '':
            calls = Call.objects.all()
        else:
            calls = Call.objects.filter(institution_id=institution_id, active=True)

        calls_dict = [{'id': call.id, 'text': str(call)} for call in calls]
        data['calls'] = calls_dict

    else:
        data['error'] = 'Invalid request'
    
    return JsonResponse(data)

# função para atualizar dinamicamente o select de call_product no form inline  
def get_products(request):
    data = {}

    if request.method == 'GET':
        call_id = request.GET.get('call_id')
        
        products = CallProduct.objects.filter(call_id=call_id)
        products_dict = [{'id': product.id, 'text': str(product)} for product in products]
        data['products'] = products_dict
    
    else:
        data['error'] = 'Invalid request'
        
    return JsonResponse(data)
    
# função para atualizar o saldo do produto
def get_balance(request):
    data = {}

    if request.method == 'GET':
        product_id = request.GET.get('product_id')

        call_product = CallProduct.objects.get(id=product_id)
        product = Product.objects.get(id=call_product.product.id)

        balance = f'{call_product.balance} {product.unit}'
        data['balance'] = balance
    
    else:
        data['error'] = 'Invalid request'

    return JsonResponse(data)

# Create para Usuário Comum
@login_required
def OrderCreate(request):
    template_name = 'order/create.html'
    context = {}
    user = request.user

    institution = user.institution
    call = Call.objects.filter(active=True, institution=institution.pk).first()
    context['call'] = call

    if call == None:
        messages.add_message(request, constants.ERROR, f"{institution} não possui uma Chamada ATIVA para Pedidos.")
        return redirect('index')

    if request.method == 'GET':
        form_product = OrderedProductFormSet()
    
    if request.method == 'POST':
        form_product = OrderedProductFormSet(request.POST)
        if form_product.is_valid():
            order = Order.objects.create(
                user=user,
                institution=institution,
                call=call
            )
            form_product.instance = order 
            form_product.save()
            
            return redirect('order-list') 
        
    context['form_product'] = form_product
    return render(request, template_name, context)      

@login_required
def OrderDetail(request, pk):
    template_name = 'order/detail.html'
    context = {}
    user = request.user

    order = get_object_or_404(Order, pk=pk)
    products = OrderedProduct.objects.filter(order=order)
    institution = get_object_or_404(Institution, pk=order.call.institution.pk)
    
    if (not user.is_staff) and (user.institution != institution):
        messages.add_message(request, constants.WARNING, "Você não tem acesso a esse Pedido.")
        return redirect('order-list')

    context['order'] = order
    context['products'] = products
    return render(request,template_name, context)

# Delete de Pedido
@login_required
@order_owner
@order_evaluated
def OrderDelete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('order-list') 
    
    return render(request, 'order/delete.html', {'order': order})

# deleta os produtos dos pedidos
@login_required
@order_owner
@order_evaluated
def OrderedProductDelete(request, pk):
    template_name = 'ordered_product/delete.html'
    context = {}

    ordered_product = get_object_or_404(OrderedProduct, pk=pk)
    context['ordered_product'] = ordered_product

    if request.method == 'POST':
        order = ordered_product.order
        ordered_product.delete()

        return redirect('detail-order', pk=order.pk)
        
    return render(request, template_name, context)

@login_required
@order_owner
@order_evaluated
def OrderedProductUpdate(request, pk):
    template_name = 'ordered_product/update.html'
    context = {}

    order = get_object_or_404(Order, pk=pk)

    if request.method == 'GET':
        products = OrderedProduct.objects.filter(order=order)
        form_product = OrderedProductFormSet(instance=order, queryset=products)
        
        context['order'] = order
        context['form_product'] = form_product
        
        return render(request, template_name, context)

    if request.method == 'POST':
        form = OrderedProductForm(request.POST, instance=order)
        form_product= OrderedProductFormSet(request.POST, instance=order)

        if form_product.is_valid():
            for form in form_product.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            form_product.save()

            return redirect('detail-order', pk=order.pk) 
        
        else:
            context['order'] = order
            context['form'] = form
            context['form_product'] = form_product

            return render(request, template_name, context)


# Avaliar pedido
@login_required
@staff_required
@order_evaluated
def EvaluateOrder(request, pk):
    template_name = 'order/evaluate-order.html'
    context = {}

    order = get_object_or_404(Order, pk=pk)
    products = OrderedProduct.objects.filter(order=order)
    
    if request.method =='GET': 
        context['order'] = order
        context['products'] = products
        return render(request, template_name, context)
    
    if request.method == 'POST': 
        for product in products:  
            form_status = request.POST.get(f'product_status_{product.pk}')  
            form_available_quantity = request.POST.get(f'product_available_quantity_{product.pk}')
            
            if form_status:
                product.status = form_status

            product_balance = int(product.call_product.balance)
            if product.status == 'available':
                product_ordered_quantity = int(product.ordered_quantity)
                product.call_product.balance = product_balance - product_ordered_quantity

            if product.status == 'parcial':
                if not form_available_quantity:
                    messages.add_message(request, constants.WARNING, f"Adicione a quantidade parcial disponível ao Produto {product.call_product.product}")
                    return redirect('evaluate-order', pk=order.pk)

                product.available_quantity = int(form_available_quantity)
                product.call_product.balance = product_balance - product.available_quantity
    
            if product.status == 'denied':
                pass

            product.call_product.save()
            product.save()

        order.status = 'approved'
        order.save()

        messages.add_message(request, constants.SUCCESS, f"Pedido avaliado com sucesso!")
        return redirect('detail-order', pk=order.pk)

@login_required
@staff_required
@order_evaluated
def EvaluateOrderDenied(request,pk):
    template_name = 'order/denied.html'
    context = {}

    order = get_object_or_404(Order, pk=pk)
    context['order'] = order

    if request.method == 'POST':
        order.status = 'denied'
        order.save()
        return redirect('detail-order', pk= order.pk) 
    
    return render(request, template_name, context)

@login_required
@order_owner
@confirm_password
def OrderDelivered(request,pk):
    template_name = 'order/delivered.html'
    context = {}

    order = get_object_or_404(Order, pk=pk)
    context['order'] = order

    if request.method == 'POST':
        order.status = 'delivered'
        order.save()
        return redirect('detail-order', pk= order.pk) 
    
    return render(request, template_name, context)