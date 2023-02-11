from django.contrib import admin
from .models import *

admin.site.register(District)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id','address_line_one','town','postcode')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Customer)
admin.site.register(Agent)


class SlotAdmin(admin.ModelAdmin):
    list_display = ('id','start_time', 'end_time')

admin.site.register(Slot,SlotAdmin)

class ViewingAdmin(admin.ModelAdmin):
    list_display = ('id','date_of_viewing','customer', 'agent','slot', 'property')

admin.site.register(Viewing,ViewingAdmin)