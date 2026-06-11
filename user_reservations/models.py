from django.db import models

class Reservation(models.Model):
    city = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    reservation_id = models.CharField(max_length=10,unique=True,editable=False,blank=True)
    user_name = models.CharField(max_length=20)
    price_per_person = models.DecimalField(max_digits=10,decimal_places=2)
    number_of_guest = models.IntegerField()
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    email =  models.EmailField()
    phone = models.CharField(max_length=15)
    check_in_date = models.CharField(max_length=15)
    tour_duration = models.CharField(max_length=10,default=None)
    tour_description = models.CharField(max_length=500,default=None)
    reservation_time = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

# Create your models here.
