from .models import Payment, PaymentMethod, Subscription, UserMembership, Membership
from django.contrib import admin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'payment_method', 'created_at', 'status', 'cart'
    ]
    search_fields = ['id']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_type']
    exclude = ['user']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_select_related = [
        'user_membership__membership', 'user_membership__user'
    ]
    list_display = [
        'user_email',
        'membership_type_name',
        'is_active',
        'is_trial',
    ]

    def user_email(self, obj):
        return obj.user_membership.user.email

    def membership_type_name(self, obj):
        return obj.user_membership.membership.get_membership_type_display()


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    pass


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass
