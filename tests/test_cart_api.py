import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from samples import sample_car, sample_user
from store.models import CarType, Dealership, Client, Order

client = APIClient()


@pytest.mark.django_db
def test_get_cart_detail():
    ...


@pytest.mark.django_db
def test_delete_order(sample_user):
    # client_ = Client.objects.create(
    #     name="User", email="ex@gmail.com", phone="+380667171304"
    # )
    # sample_car_type = CarType.objects.create(
    #     name="CarType1", brand="Brand1", price=10000
    # )
    # dealer = Dealership.objects.create(id=1, name="Dealer")
    # dealer.clients.add(client_)
    # dealer.available_car_types.set([sample_car_type])
    #
    # order = Order(id=1, client=client_, dealership=dealer, is_paid=False)
    #
    # url = reverse("cart-detail", args=[order.order_id])
    # response = client.delete(url)
    #
    # assert response.status_code == status.HTTP_204_NO_CONTENT
    ...