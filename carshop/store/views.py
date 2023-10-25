from django.shortcuts import render, redirect

from store.forms import ClientForm, CarTypeForm, CarForm, DealershipForm
from store.models import Car, CarType, Dealership

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


def sell_car(request):
    ...


""" --- STAFF PART --- """


# ADD METHODS
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
    if request.method == "GET":
        form = CarForm
        return render(request, "add_car.html", {"car": form})

    form = CarForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("get_all_cars")

    return render(request, "add_car.html", {"car": form})


def add_dealership(request):
    if request.method == "GET":
        form = DealershipForm
        return render(request, "add_dealership.html", {"dealer": form})

    form = DealershipForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("get_all_dealership")

    return render(request, "add_dealership.html", {"dealer": form})


# GET METHODS
def get_all_types_of_cars(request):
    car_type_list = CarType.objects.all()
    return render(request, "all_types_of_cars.html", {"car_type": car_type_list})


def get_all_cars(request):
    car_list = Car.objects.all()
    return render(request, "all_cars.html", {"car": car_list})


def get_all_dealership(request):
    dealership_list = Dealership.objects.all()
    return render(request, "all_dealers.html", {"dealer": dealership_list})
