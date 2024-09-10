from django.contrib import admin
from .models import Stad, Hotel

class StadAdmin(admin.ModelAdmin):
    list_display = ('naam', 'achtergrond_afbeelding')  # Lijstweergave van de steden

class HotelAdmin(admin.ModelAdmin):
    list_display = ('naam', 'stad')  # Lijstweergave hotels en de gekoppelde stad 

admin.site.register(Stad, StadAdmin)
admin.site.register(Hotel, HotelAdmin)


