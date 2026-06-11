from django.db import models
from tinymce.models import HTMLField

class BestOfferDeals(models.Model):
    bod_img = models.FileField(max_length=200,upload_to='best_offers_deals/')
    bod_offer = models.CharField(max_length=50)
    bod_city_name = models.CharField(max_length=50)
    bod_tour_duration = models.CharField(max_length=50)
    bod_des = models.CharField(max_length=200)
    bod_price = models.DecimalField(max_digits=10,decimal_places=2)
    bod_tour_description = HTMLField(default='hello')

# Create your models here.
