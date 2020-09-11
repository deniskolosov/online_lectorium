from .models import Payment, PaymentMethod
from django.contrib import admin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_method', 'created_at', 'status', 'payment_for',]
    search_fields = ['id']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_type']
    exclude = ['user']
