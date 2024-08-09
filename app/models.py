from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Institution(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Instituição")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

    @property
    def users(self):
        if self.id:
            users = UserProfile.objects.filter(institution=self.id)
            return users

    @property
    def calls(self):
        if self.id:
            calls = Call.objects.filter(institution=self.id)
            return calls


class UserProfile(AbstractUser):
    username = models.EmailField(verbose_name="Email", max_length=150, unique=True)
    first_name = models.CharField(verbose_name="Nome Completo", max_length=150)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True, verbose_name="Instituição")

    REQUIRED_FIELDS = ["institution", "first_name"]

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['-id']


class Call(models.Model):
    number = models.CharField(max_length=50, verbose_name="Número")
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, verbose_name="Instituição")
    start = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data de Início")
    end = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data de Término")
    active = models.BooleanField(default=False, verbose_name="Situação")

    def __str__(self):
        return f'Chamada - {self.number} de {self.institution.name}'

    def clean(self):
        if self.active:
            active_calls = Call.objects.filter(institution=self.institution, active=True)
            if self.pk:
                active_calls = active_calls.exclude(pk=self.pk)
            if active_calls.exists():
                raise ValidationError("Já existe uma chamada ativa para esta instituição.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

    @property
    def products(self):
        if self.id:
            products = CallProduct.objects.filter(call=self.id)
            return products

class Product(models.Model):
    CHOICES = [
        ('KG', 'KG'),
        ('UNI', 'UNI'),
        ('BDJ', 'BDJ'),
        ('L', 'L'),
    ]
    name = models.CharField(max_length=100, verbose_name="Nome do Produto")
    unit = models.CharField(max_length=3, choices=CHOICES, verbose_name="Unidade de Medida")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class CallProduct(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='product', verbose_name="Chamada")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='call', verbose_name="Produto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    balance = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Saldo")

    def __str__(self):
        return f'{self.product} {self.price} - {self.call.number}'

    class Meta:
        ordering = ['-id']


class Order(models.Model):
    CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('denied', 'Negado'),
        ('delivered', 'Entregue'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name="Autor")
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, verbose_name="Instituição")
    call = models.ForeignKey(Call, on_delete=models.PROTECT, verbose_name="Chamada")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Timestamp")
    status = models.CharField(max_length=10, choices=CHOICES, default='pending', verbose_name="Situação")

    def __str__(self):
        return f'Pedido de {self.institution} (Chamada {self.call.number}) feito por {self.user}'

    class Meta:
        ordering = ['-timestamp']

    @property
    def products(self):
        if self.id:
            products = OrderedProduct.objects.filter(order=self.id)
            return products

    @property
    def available_products(self):
        if (self.status == 'approved') or (self.status == 'delivered') :
            products = OrderedProduct.objects.filter(
                order=self,
                status__in=('parcial', 'available')
            )
            return products

    @property
    def get_total_price(self):
        total_price = 0.0
        if self.id:
            products = self.available_products
            for product in products:
                total_price += float(product.get_quantity_price.replace(',', '.'))
        return "{:.2f}".format(total_price).replace('.', ',') if total_price else None

    @property
    def request_products(self):
        if (self.status == 'approved') or (self.status == 'pending') :
            products = OrderedProduct.objects.filter(
                order=self,
                status__in=('parcial', 'available')
            )
            return products


class OrderedProduct(models.Model):
    CHOICES = [
        ('parcial', 'Parcial'),
        ('available', 'Disponível'),
        ('denied', 'Negado'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='call_products', verbose_name="Pedido")
    call_product = models.ForeignKey(CallProduct, on_delete=models.PROTECT, related_name='order', verbose_name="Produto da Chamada")
    ordered_quantity = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Quant. Pedida")
    available_quantity = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Quant. Disponível")
    status = models.CharField(max_length=10, choices=CHOICES, default='available', verbose_name="Situação")

    def __str__(self):
        return f'({self.order}) ({self.call_product}) ({self.ordered_quantity})'

    class Meta:
        ordering = ['-id']

    @property
    def get_quantity_price(self):
        quantity_price = None
        if self.call_product and (self.ordered_quantity or self.available_quantity):
            price = float(self.call_product.price)
            quantity = float(self.ordered_quantity)
            if self.available_quantity:
                quantity = float(self.available_quantity)
            quantity_price = price*quantity
        return "{:.2f}".format(quantity_price).replace('.', ',') if quantity_price is not None else None