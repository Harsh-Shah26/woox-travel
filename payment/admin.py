from django.contrib import admin
from payment.models import UserPayment

class UserPaymentlist(admin.ModelAdmin):
    list_display = (
        'id',
        'reservation_id',
        'reservation_user_id',
        'payment_id',
        'username',
        'user_destination',
        'user_total_payment',
        'user_pay_method',
        'payment_time',
        'user_invoice',
        )
    
admin.site.register(UserPayment,UserPaymentlist)

# Register your models here.
