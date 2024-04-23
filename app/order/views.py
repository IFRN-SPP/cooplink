from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from ..forms import OrderForm, OrderedProductFormSet, OrderedProductForm
from ..models import Call, CallProduct, Order, OrderedProduct, Product

# CRUD Pedidos

@login_required
def OrderList(request):
    order = Order.objects.all()
    context = {'order_list': order}
    return render(request, 'order/list.html', context)

# Create para Admin
@login_required
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

        if form.is_valid() and form_product.is_valid():
            user = request.user
            form.instance.user = user
            order = form.save()
            form_product.instance = order 
            form_product.save()
            
            return redirect('order-list') 
        
        else:
            context['form'] = form 
            context['form_product'] = form_product

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
def OrderCreate(request):
    template_name = 'order/create.html'
    context = {}

    user = request.user
    institution = user.institution
    call = Call.objects.filter(active=True, institution=institution.pk).first()
    
    if request.method == 'GET':
        form_product_factory = OrderedProductFormSet
        form_product = form_product_factory()
        
        context['call'] = call
        context['form_product'] = form_product
        
        return render(request, template_name, context)
    
    if request.method == 'POST':
        form_product_factory = OrderedProductFormSet
        form_product = form_product_factory(request.POST)

        if form_product.is_valid():
            order = Order.objects.create(
                user=user,
                institution=institution,
                call=call
            )

            form_product.instance = order 
            form_product.save()
            
            return redirect('order-list') 
        
        else:
            context['call'] = call
            context['form_product'] = form_product

            return render(request, template_name, context)    

@login_required
def OrderDetail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    products = OrderedProduct.objects.filter(order=order)
    context = {
        'order': order, 
        'products': products,
    }
    return render(request, 'order/detail.html', context)

# deleta os pedidos, não os produtos dos pedidos em especifico
def OrderDelete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order-list') 
    return render(request, 'order/delete.html', {'order': order})

# deleta os produtos dos pedidos
@login_required
def OrderedProductDelete(request, pk):
    ordered_product = get_object_or_404(OrderedProduct, pk=pk)
    if request.method == 'POST':
        ordered_product.delete()
        return redirect('detail-order', pk= ordered_product.order.pk) # retorna para a página da chamada
    return render(request, 'ordered_product/delete.html', {'ordered_product':  ordered_product})

@login_required
def OrderedProductUpdate(request, pk):
    # pego a pk do pedido, na qual quero editar os produtos
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'GET':
        # obtém todos os produtos relacionados ao pedido
        products = OrderedProduct.objects.filter(order=order)
        form_product_factory = OrderedProductFormSet
        form_product = form_product_factory(instance=order, queryset=products)
        context = {
            'order': order,
            'form_product': form_product,
        }
        return render(request, 'ordered_product/update.html', context)

    # Se o método for POST, processa os dados submetidos
    if request.method == 'POST':
        form = OrderedProductForm(request.POST, instance=order)
        form_product_factory = OrderedProductFormSet 
        form_product = form_product_factory(request.POST, instance=order)

        if form_product.is_valid():
            # deleta os produtos que foram excluidos
            for form in form_product.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            form_product.save()
            return redirect('detail-order', pk=order.pk)  # Redireciona para a página do pedido
        else:
            context = {
                'order': order,
                'form': form,
                'form_product': form_product,
            }
            return render(request, 'ordered_product/update.html', context)

# Avaliar pedido

def EvaluateOrder(request, pk):
    #pego a pk e seus produtos
    order = get_object_or_404(Order, pk=pk)
    products = OrderedProduct.objects.filter(order=order)
    
    if request.method =='GET': #caso for get apenas renderizo
        context = {
            'order': order, 
            'products': products,
        }
        return render(request, 'order/evaluate-order.html', context)
    
    if request.method == 'POST': #se for post
        for product in products: #para produto em produtos do pedido 
            new_status = request.POST.get(f'product_status_{product.pk}') #recupero o valor que foi selecionado 
            if new_status is not None: #se não for None, significa que tem um novo status
                product.status = new_status
                product.save()
        order.status = 'approved'
        order.save()
        return redirect('detail-order', pk=order.pk)
    
def EvaluateOrderDenied(request,pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.status = 'denied'
        order.save()
        return redirect('detail-order', pk= order.pk) 
    return render(request, 'order/denied.html', {'order':  order })