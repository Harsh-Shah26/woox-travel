# from django.contrib import admin
# from cities_towns_about.models import AboutCityTown

# class CityTown(admin.ModelAdmin):
#     list_display = ('id','act_img','act_city_name','act_price','act_tour_duration','act_tour_description')


# admin.site.register(AboutCityTown,CityTown)

# Register your models here.


# added by me
from django.contrib import admin
from .models import AboutCityTown, CityPlace


class CityPlaceInline(admin.TabularInline):
    model = CityPlace
    extra = 4


@admin.register(AboutCityTown)
class AboutCityTownAdmin(admin.ModelAdmin):
    list_display = ('id', 'act_city_name', 'act_price', 'act_tour_duration')
    list_display_links = ('id', 'act_city_name')
    search_fields = ('act_city_name',)
    inlines = [CityPlaceInline]


@admin.register(CityPlace)
class CityPlaceAdmin(admin.ModelAdmin):
    list_display = ('place_name', 'city')
    list_filter = ('city',)
    search_fields = ('place_name', 'city__act_city_name')