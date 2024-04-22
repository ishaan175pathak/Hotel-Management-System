import json
from django.urls import reverse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import ReviewSerializer
from typing import List

# Create your views here.

def index(request):
    return render(request, "index.html")

def aboutUs(request):
    return render(request, "about.html")

def contactUs(request):
    return render(request, "contact.html")

def login(request):
    if request.method == "GET":
        global url
        url = request.GET.get("next", "Not Available")
        return render(request, "login.html")
    
    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        
        if user is not None:
            auth_login(request, user)
            if url != "Not Available":
                return redirect(url)
            
            return redirect(reverse("login"))
        
        else:
            return render(request, "login.html", {"context": "Try Again", "class": "alert alert-danger"})

def register(request):
    if request.method == "POST":
        
        username = request.POST.get("username")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        
        try:
            user, result = get_user_model().objects.get_or_create(username = username, password = password, email = email, first_name = firstName, last_name = lastName)
            
            if result:
                customer = Customer(customer = user, phone_number = phone)
                customer.save()

            return redirect(reverse("login"))
        except:
            return render(request, "login.html", {"context": "try again", "class": "alert alert-danger"})

@login_required(login_url="/login user/")
def reservation(request, room_number: str):
    user = get_object_or_404(User, username = request.user)
    customer = get_object_or_404(Customer, customer = user)
    if request.method == "GET":
        return render(request, "reservation.html", {"customer_name": customer.customer.get_full_name(), "customer_email": customer.customer.email, "customer": customer, "room_number": room_number})
    
    elif request.method == "POST":

        room_number = int(room_number)
        adult = request.POST.get("adults")
        children = request.POST.get("children")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        print(f"{room_number=}")
        print(f"{adult=}")
        print(f"{children=}")
        print(f"{check_in=}")
        print(f"{check_out=}")

        try:
            if Rooms.objects.filter(room_number = room_number):
                room = get_object_or_404(Rooms, room_number = room_number)
                roomBooking = RoomBooking(room = room, customer = customer, adult = adult, children = children, check_in = check_in, check_out = check_out)
                roomBooking.save()

                return render(request, "reservation.html", {"context": "success"})
                
            else:
                raise Exception("Room not found")
        except Exception as exp:
            return render(request, "reservation.html")

def room(request):
    if request.method == "GET":
        rooms = Rooms.objects.all()
        return render(request, "rooms.html", {"rooms": rooms})

@login_required(login_url="/login user/")
def food(request):
    if request.method == "GET":
        food_menu = Menu.objects.all()
        user = get_object_or_404(User, username = request.user)
        customer = get_object_or_404(Customer, customer = user)
        bookedRoom = get_object_or_404(RoomBooking, customer = customer)
        return render(request, "food_menu.html", {"menu": food_menu, "room_number": bookedRoom.room.room_number, "user_info": user.get_username()})

@csrf_exempt
def bookFood(request, room: int):
    if request.method == "POST":
        message = dict(JSONParser().parse(request))
        print(message)

        for values in message["items"]:
            item_name, item_quantity, item_price = values
            try:
                obj = FoodBooking(room_details = room, customer_name = message["user"], item_name = item_name, item_quantity = int(item_quantity), item_price = int(item_price))
                obj.save()

            except:
                return JsonResponse(json.dumps({"status": "Not Received"}), safe = False)

        return JsonResponse(json.dumps({"status": "received Data"}), safe=False)
    
def review(request):
    if request.method == "GET":
        all_data: List[Review] = Review.objects.all()
        print(all_data)
        serialized_data: List[ReviewSerializer] = ReviewSerializer(all_data, many= True)
        return JsonResponse(serialized_data.data, safe=False)
    
def Logout(request):
    logout(request)

    return redirect(reverse("home"))