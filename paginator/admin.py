from django.contrib import admin
from paginator.models import Paginator

class PaginatorAdmin(admin.ModelAdmin):
    list_display = ('paginator_title','paginator_des')
    
admin.site.register(Paginator,PaginatorAdmin)
# Register your models here.
