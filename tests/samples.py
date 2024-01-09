import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from store.models import CarType, Car


@pytest.fixture
def sample_car():
    car_type = CarType.objects.create(id=1, name="X5", brand="BMW", price=90000)
    car = Car.objects.create(car_type=car_type, color="Black", year=2024, image=None)
    return car


@pytest.fixture
def sample_user():
    client = APIClient()
    user = User(username="User", password="UserPassword")
    client.force_authenticate(user)
    return client
