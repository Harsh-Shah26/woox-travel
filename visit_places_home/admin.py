from django.contrib import admin
from .models import VisitPlaceHome

# added by me : Visit Places Home admin
@admin.register(VisitPlaceHome)
class VisitHome(admin.ModelAdmin):
    list_display = ('id','vph_place','vph_country','vph_price')
    search_fields = ('vph_place',)
    list_display_links = ('vph_place','id')

    