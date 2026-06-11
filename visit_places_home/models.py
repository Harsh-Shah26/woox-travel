from django.db import models
from tinymce.models import HTMLField

class VisitPlaceHome(models.Model):
    vph_img = models.FileField(max_length=200,upload_to='visit_place_home/')
    vph_place = models.CharField(max_length=50)
    vph_country = models.CharField(max_length=50)
    vph_des = HTMLField()
    vph_people = models.FloatField(max_length=10)
    vph_km = models.FloatField(max_length=10)
    vph_price = models.FloatField(max_length=10)


    def __str__(self):
        return self.vph_place


# Create your models here.
