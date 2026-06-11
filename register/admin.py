from django.contrib import admin
from register.models import Register

class RegisterUser(admin.ModelAdmin):
    list_display = ('id','username','firstname','lastname','email','password')

admin.site.register(Register,RegisterUser)

# Register your models here.
