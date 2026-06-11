from django.db import models
from tinymce.models import HTMLField

class BestOffersAbout(models.Model):
    boa_img = models.FileField(max_length=200,upload_to='best_offers_about/')
    boa_city_name = models.CharField(max_length=50)
    boa_check_ins = models.IntegerField()
    boa_price = models.DecimalField(max_digits=10,decimal_places=2)
    boa_tour_duratrions = models.CharField(max_length=40,null=True,blank=True)
    boa_tour_description = HTMLField(default="hello")

# Create your models here.
