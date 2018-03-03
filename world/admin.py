from django.contrib import admin

# Register your models here.
from world.models import Country


class CountryAdmin(admin.ModelAdmin):
    model = Country

    list_display = ('name', 'code', 'latitude', 'longitude')

admin.site.register(Country, CountryAdmin)