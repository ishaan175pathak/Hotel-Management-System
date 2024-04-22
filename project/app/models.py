from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=False)

    def __str__(self) -> str:
        return f"   customer first name - {self.customer.first_name} | \
                    customer last name - {self.customer.last_name} | \
                    customer username - {self.customer.get_username()} | \
                    phone number - {self.phone_number}"

class Menu(models.Model):
    item_name = models.CharField(max_length=1000, blank=True)
    item_price = models.IntegerField(blank=False)
    item_image = models.ImageField(upload_to="menu/")

    def __str__(self) -> str:
        return f"   item_name - {self.item_name} | \
                    item_price - {self.item_price} | \
                    item_image - {self.item_image}"

class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, blank=False)

    def __str__(self) -> str:
        return f"   user - {self.user.customer.first_name} | \
                    review - {self.review}"

class Rooms(models.Model):

    availablity = (
        ("available", "available"),
        ("unavailable", "unavailable")
    )

    types = (
        ("suite", "Suite"),
        ("premium", "Premium"),
        ("standard", "Standard"),
        ("dormitory", "Dormitory")
    )

    features = (
        ("free breakfast", "Free Breakfast"),
        ("free internet", "Free Internet"),
        ("lunch included", "Lunch Included"),
    )

    room_image = models.ImageField(upload_to="hotel images/", blank=True)
    room_number = models.BigAutoField(primary_key=True, unique=True)
    beddings = models.IntegerField(default=1, blank=False)
    room_type = models.CharField(choices=types, blank=False, max_length=100)
    features = models.CharField(choices=features, blank=False, max_length=100)
    room_status = models.CharField(choices=availablity, blank=False, max_length=100) 
    
    def __str__(self) -> str:
        return f"   room_number - {self.room_number} | \
                    room_image - {self.room_image} | \
                    beddings - {self.beddings} | \
                    room_type - {self.room_type} | \
                    features - {self.features} | \
                    room_status - {self.room_status}"
    
class RoomBooking(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    adult = models.IntegerField(default=1, blank=False)
    children = models.IntegerField(default=0, blank=False)
    check_in = models.DateField(default= date.today(), blank=False)
    check_out = models.DateField(blank=False)

    def __str__(self) -> str:
        return f"   room - {self.room} | \
                    customer - {self.customer} | \
                    adult - {self.adult} | \
                    children - {self.children} | \
                    check_in - {self.check_in} | \
                    check_out - {self.check_out}"

class FoodBooking(models.Model):
    room_details = models.IntegerField(default=101, blank=False)
    customer_name = models.CharField(max_length=1000, blank=False)
    item_name = models.CharField(max_length=1000, blank=False)
    item_price = models.IntegerField(blank=False)
    item_quantity = models.IntegerField(blank=False)
    date = models.DateField(default=date.today())

    def __str__(self) -> str:
        return f"   room_number- {self.room_details} | \
                    customer_name - {self.customer_name} | \
                    item_name - {self.item_name} | \
                    item_price - {self.item_price} | \
                    item_quantity - {self.item_quantity} | \
                    date  - {self.date}"