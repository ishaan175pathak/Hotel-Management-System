from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Review)
admin.site.register(Rooms)
admin.site.register(FoodBooking)
admin.site.register(RoomBooking)