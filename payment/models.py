from django.db import models


class UserPayment(models.Model):
    reservation_id = models.CharField(max_length=10,editable=False)
    reservation_user_id = models.IntegerField(editable=False)
    payment_id = models.CharField(max_length=5,unique=True,editable=False,blank=True)
    username = models.CharField(editable=False,max_length=50)
    user_destination = models.CharField(editable=False,max_length=50) 
    user_total_payment = models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    user_pay_method = models.CharField(editable=False,max_length=10)
    payment_time = models.DateTimeField(editable=False)
    user_invoice = models.FileField(max_length=200,upload_to='invoice/',default=None)


# Create your models here.
