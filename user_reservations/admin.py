from django.contrib import admin
from user_reservations.models import Reservation

class MakeReservation(admin.ModelAdmin):
    list_display = ('reservation_id','city','username','user_name','price_per_person','number_of_guest','total_price','email','phone','check_in_date','tour_duration','reservation_time','payment_status')

admin.site.register(Reservation,MakeReservation)

# Register your models here.
