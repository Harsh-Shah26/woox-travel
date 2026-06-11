from django.contrib import admin
from best_offers_about.models import BestOffersAbout

class BestOffers(admin.ModelAdmin):
    list_display = ('id','boa_img','boa_city_name','boa_check_ins','boa_price','boa_tour_duratrions','boa_tour_description')
    
    list_display_links = ('id', 'boa_city_name')

admin.site.register(BestOffersAbout,BestOffers)

# Register your models here.
