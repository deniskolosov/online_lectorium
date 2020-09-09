from django.contrib import admin
from .models import Ticket, QRCode


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'scanned']
