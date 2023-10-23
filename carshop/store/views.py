from django.shortcuts import render, redirect

from store.forms import ClientForm, CarTypeForm, CarForm
from store.models import Car, CarType

""" --- CLIENT PART --- """


def register_client(request):
    if request.method == "GET":
        form = ClientForm
        return render(request, "add_client.html", {"client": form})

    form = ClientForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("redirect_on_store_page")

    return render(request, "add_client.html", {"client": form})


def redirect_on_store_page(request):
    car_list = Car.objects.all()
    return render(request, "store_page.html", {"cars": car_list})


""" --- STAFF PART --- """


def get_all_types_of_cars(request):
    car_type_list = CarType.objects.all()
    return render(request, "all_types_of_cars.html", {"car_type": car_type_list})


def add_new_car_type(request):
    if request.method == "GET":
        form = CarTypeForm
        return render(request, "add_car_type.html", {"car_type": form})

    form = CarTypeForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("get_all_types_of_cars")

    return render(request, "add_car_type.html", {"car_type": form})


def add_new_car(request):
    ...
