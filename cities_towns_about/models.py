# from django.db import models
# from tinymce.models import HTMLField


# class AboutCityTown(models.Model):
#     act_img = models.FileField(max_length=200,upload_to='about_cities_towns/')
#     act_city_name = models.CharField(max_length=50)
#     act_price = models.DecimalField(max_digits=10,decimal_places=2)
#     act_tour_duration = models.CharField(max_length=50,null=True,blank=True)
#     act_tour_description = HTMLField(default="hello")
    
#     def __str__(self):
#         return self.act_city_name

# # Create your models here.


# added by me

# added by me
from django.db import models
from tinymce.models import HTMLField


class AboutCityTown(models.Model):
    act_img = models.FileField(max_length=200, upload_to='about_cities_towns/')
    act_img2 = models.FileField(max_length=200, upload_to='about_cities_towns/', null=True, blank=True)
    act_img3 = models.FileField(max_length=200, upload_to='about_cities_towns/', null=True, blank=True)
    act_img4 = models.FileField(max_length=200, upload_to='about_cities_towns/', null=True, blank=True)
    act_img5 = models.FileField(max_length=200, upload_to='about_cities_towns/', null=True, blank=True)

    act_city_name = models.CharField(max_length=50)
    act_price = models.DecimalField(max_digits=10, decimal_places=2)
    act_tour_duration = models.CharField(max_length=50, null=True, blank=True)
    act_tour_description = HTMLField(default="hello")

    def __str__(self):
        return self.act_city_name
    


# each city ke specific places
class CityPlace(models.Model):
    city = models.ForeignKey('AboutCityTown', on_delete=models.CASCADE, related_name='places')
    place_name = models.CharField(max_length=200)
    place_image = models.ImageField(upload_to='city_places/')
    place_description = models.TextField()

    def __str__(self):
        return f"{self.city.act_city_name} - {self.place_name}"