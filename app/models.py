from django.db import models
from django.contrib.auth.models import AbstractUser

class Institution(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)

    def __str__(self):
        return self.name

class UserProfile(AbstractUser):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

class Call(models.Model):
    number = models.CharField( max_length=50)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    start = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Chamada - {self.number}'

class Product(models.Model):
    CHOICES = [
        ('KG', 'KG'),
        ('UNI', 'UNI'),
    ]
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=3, choices=CHOICES)

    def __str__(self):
        return self.name

class CallProduct(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='call')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product} {self.price} - {self.call.number}'

class Order(models.Model):
    CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('delivered', 'Entregue'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES, default='pending')

    def __str__(self):
        return f'{self.user} - {self.institution} - {self.call.number}'

class OrderedProduct(models.Model):
    CHOICES = [
        ('parcial', 'Parcial'),
        ('available', 'Disponível'),
        ('denied', 'Negado'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='call_products')
    call_product = models.ForeignKey(CallProduct, on_delete=models.CASCADE, related_name='order')
    ordered_quantity = models.IntegerField(default=0) 
    available_quantity = models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=CHOICES, default='available')

    def __str__(self):
        return f'({self.order}) ({self.call_product}) ({self.quantity})'
    