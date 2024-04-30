from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class Institution(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Instituição")
    cnpj = models.CharField(max_length=14, verbose_name="CNPJ")

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, null=True, verbose_name="Instituição")

    def __str__(self):
        return self.username

class Call(models.Model):
    number = models.CharField(max_length=50, verbose_name="Número")
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, verbose_name="Instituição")
    start = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data de Início")
    end = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data de Término")
    active = models.BooleanField(default=False, verbose_name="Situção")

    def __str__(self):
        return f'Chamada - {self.number}'
    
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
        
        
class Product(models.Model):
    CHOICES = [
        ('KG', 'KG'),
        ('UNI', 'UNI'),
    ]
    name = models.CharField(max_length=100, verbose_name="Nome do Produto")
    unit = models.CharField(max_length=3, choices=CHOICES, verbose_name="Unidade de Medida")

    def __str__(self):
        return self.name

class CallProduct(models.Model):
    call = models.ForeignKey(Call, on_delete=models.PROTECT, related_name='products', verbose_name="Chamada")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='call', verbose_name="Produto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    balance = models.IntegerField(default=None, verbose_name="Saldo")

    def __str__(self):
        return f'{self.product} {self.price} - {self.call.number}'

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
        return f'{self.user} - {self.institution} - {self.call.number}'

class OrderedProduct(models.Model):
    CHOICES = [
        ('parcial', 'Parcial'),
        ('available', 'Disponível'),
        ('denied', 'Negado'),
    ]

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='call_products', verbose_name="Pedido")
    call_product = models.ForeignKey(CallProduct, on_delete=models.PROTECT, related_name='order', verbose_name="Produto da Chamada")
    ordered_quantity = models.IntegerField(default=None, verbose_name="Quant. Pedida") 
    available_quantity = models.IntegerField(null=True, blank=True, verbose_name="Quant. Disponível")
    status = models.CharField(max_length=10, choices=CHOICES, default='available', verbose_name="Situção")

    def __str__(self):
        return f'({self.order}) ({self.call_product}) ({self.ordered_quantity})'
    