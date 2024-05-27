from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Product)
admin.site.register(Institution)

# Cria formuçários inline no admin do Django, apenas para testes 
class CallProductInline(admin.TabularInline):
    model = CallProduct
    extra = 1

class CallAdmin(admin.ModelAdmin):
    inlines = [CallProductInline]

admin.site.register(Call, CallAdmin)

class OrderedProductInline(admin.TabularInline):
    model = OrderedProduct
    extra = 1
    #  Função que associa Produtos da Chamada  com a Chamada do Pedido, apenas para testes no admin do Django
    def get_formset(self, request, obj=None, **kwargs):
      formset = super().get_formset(request, obj, **kwargs)
      if obj:
          formset.form.base_fields['call_product'].queryset = CallProduct.objects.filter(call=obj.call)
      return formset

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderedProductInline]
    
admin.site.register(Order, OrderAdmin)