from django.contrib import admin
from best_offers_deals.models import BestOfferDeals

class Best_offer_delas(admin.ModelAdmin):
    list_display = ('id','bod_img','bod_offer','bod_city_name','bod_tour_duration','bod_des','bod_price','bod_tour_description')

    list_display_links = ('id', 'bod_city_name')
    
admin.site.register(BestOfferDeals,Best_offer_delas)

# Register your models here.

