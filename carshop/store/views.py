from django.shortcuts import render, redirect, reverse

from store.forms import ClientForm
from store.models import Car


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
