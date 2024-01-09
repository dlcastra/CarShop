import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from samples import sample_car, sample_user
from store.models import CarType, Dealership, Client

client = APIClient()


@pytest.mark.django_db
def test_get_order():
    url = reverse("buy-car-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_order_detail(sample_car):
    url = reverse("buy-car-detail", args=[sample_car.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": sample_car.id,
        "car_type": sample_car.car_type.id,
        "color": sample_car.color,
        "year": sample_car.year,
        "image": sample_car.image,
    }


@pytest.mark.django_db
def test_create_order(sample_user, sample_car):
    client_ = Client.objects.create(
        name="User", email="ex@gmail.com", phone="+380667171304"
    )

    sample_car_type = CarType.objects.create(
        name="CarType", brand="Brand1", price=10000
    )
    dealer = Dealership.objects.create(name="Dealer")
    dealer.clients.add(client_)
    dealer.available_car_types.set([sample_car_type])

    sample_car.car_type.dealerships.add(dealer)
    sample_car.save()

    url = reverse("buy-car-detail", args=[sample_car.id])
    response = sample_user.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert "Car was added to your cart" in response.data.get("message", "")


@pytest.mark.django_db
def test_method_not_allowed(sample_user, sample_car):
    url = reverse("buy-car-detail", args=[sample_car.id])
    response = sample_user.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.status_code != status.HTTP_204_NO_CONTENT
