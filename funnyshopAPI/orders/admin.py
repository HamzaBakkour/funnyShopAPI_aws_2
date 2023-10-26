from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'first_name',
                    'last_name',
                    'paid',
                    'stripe_id',
                    'created',
                    'updated']
    
    list_filter = ['created', 'updated']
    search_fields = ['id', 'first_name']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['id', 'order__id', 'product__name']
