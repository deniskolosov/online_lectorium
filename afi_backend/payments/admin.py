from .models import Payment, PaymentMethod
from django.contrib import admin


#TODO: Register Payment and Payment method

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_method', 'created_at', 'status']
    search_fields = ['id']
    readonly_fields = ['payment_method']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_type']
    exclude = ['user']
