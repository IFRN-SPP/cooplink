from django.db import models
from django.contrib.auth.models import User

class Institution(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Call(models.Model):
    number = models.CharField( max_length=50)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    start = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Chamada - {self.number}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CallProduct(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    call_product = models.ForeignKey(CallProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0) 

    def __str__(self):
        return f'({self.order}) ({self.call_product}) ({self.quantity})'
    