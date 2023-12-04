from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.core.signing import Signer, BadSignature
from django.shortcuts import render, redirect, get_object_or_404

from store.forms import (
    ClientForm,
    CarTypeForm,
    CarForm,
    DealershipForm,
    UserCreationFormWithEmail,
)
from store.models import Car, CarType, Dealership, Client, Order, OrderQuantity

""" --- CLIENT PART --- """


def create_client(request):
    if request.method == "GET":
        form = ClientForm()
        return render(request, "add_client.html", {"client": form})

    form = ClientForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("redirect_on_store_page")

    return render(request, "add_client.html", {"client": form})


# Send auth link
def send_activation_email(request, user: User):
    user_signed = Signer().sign(user.id)
    signed_url = request.build_absolute_uri(f"/activate/{user_signed}")
    send_mail(
        "Registration complete",
        "Click here to activate your account: " + signed_url,
        "1dlcastra@gmail.com",
        [user.email],
        fail_silently=False,
    )


def register_view(request):
    if request.method == "GET":
        form = UserCreationFormWithEmail()
        return render(request, "registration/register.html", {"form": form})

    form = UserCreationFormWithEmail(request.POST)
    if form.is_valid():
        form.instance.is_active = False
        form.save()
        send_activation_email(request, form.instance)
        return redirect("login_view")

    return render(request, "registration/register.html", {"form": form})


def activate(request, user_signed):
    try:
        user_id = Signer().unsign(user_signed)
    except BadSignature:
        return redirect("login_view")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login_view")
    user.is_active = True
    user.save()
    return redirect("login_view")


def redirect_on_store_page(request):
    car_list = Car.objects.filter(owner__isnull=True, blocked_by_order__isnull=True)
    return render(request, "store_page.html", {"cars": car_list})


def create_order(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.blocked_by_order or car.owner:
        return redirect("redirect_on_store_page")

    if request.method == "POST":
        client = Client.objects.first()
        order, created = Order.objects.get_or_create(
            client=client, dealership=car.car_type.dealerships.first(), is_paid=False
        )
        car_type = car.car_type
        order_quantity, _ = OrderQuantity.objects.get_or_create(
            order=order, car_type=car_type
        )
        car.block(order)
        client.order_cart.add(car)

    return redirect("redirect_on_store_page")


def view_cart(request):
    if request.method == "GET":
        return redirect(redirect_on_store_page)
    if request.method == "POST":
        client = Client.objects.first()
        user_cars = client.order_cart.all()
        order = Order.objects.filter(client=client, is_paid=False).first()
        return render(
            request, "cart_page.html", {"user_cars": user_cars, "order": order}
        )


def pay_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "GET":
        return render(request, "order_success.html")

    if request.method == "POST":
        if not order.is_paid:
            client = Client.objects.first()
            cars = Car.objects.filter(blocked_by_order=order)
            for car in cars:
                car.sell()
                car.owner = client
                car.save()
            order.is_paid = True
            order.save()
            client.order_cart.clear()

            return render(request, "order_success.html")
        return render(request, "order_success.html")


def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "GET":
        return render(request, "order_cancel.html")

    if request.method == "POST":
        cars = Car.objects.filter(blocked_by_order=order)
        for car in cars:
            car.unblock()
        order.delete()

        return render(request, "order_cancel.html")

    return render(request, "order_cancel.html")


""" --- STAFF PART --- """


# ADD METHODS
def add_new_car_type(request):
    if request.method == "GET":
        form = CarTypeForm()
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
        form = DealershipForm()
        return render(request, "add_dealership.html", {"dealer": form})

    form = DealershipForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("get_all_dealership")

    return render(request, "add_dealership.html", {"dealer": form})


# GET METHODS
def get_all_types_of_cars(request):
    if request.method == "GET":
        car_type_list = CarType.objects.all()
        return render(request, "all_types_of_cars.html", {"car_type": car_type_list})


def get_all_cars(request):
    car_list = Car.objects.all()
    return render(request, "all_cars.html", {"car": car_list})


def get_all_dealership(request):
    dealership_list = Dealership.objects.all()
    return render(request, "all_dealers.html", {"dealer": dealership_list})
