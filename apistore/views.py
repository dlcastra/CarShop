from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from store.models import Car, Dealership, CarType, Client, Order, OrderQuantity

from apistore.serializers import (
    CarSerializer,
    DealershipSerializer,
    CarTypeSerializer,
)


# GET AND POST METHODS


class CarTypeViewSet(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    GenericViewSet,
):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CarViewSet(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    GenericViewSet,
):
    queryset = Car.objects.filter(owner__isnull=True, blocked_by_order__isnull=True)
    serializer_class = CarSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DealersViewSet(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    GenericViewSet,
):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# class BuyCarView(APIView):
#     def post(self, request, pk):
#         car = get_object_or_404(Car, pk=pk)
#         if car.blocked_by_order or car.owner:
#             return Response(
#                 {"error": "Car is blocked or already owned"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         client = Client.objects.first()
#         order, created = Order.objects.get_or_create(
#             client=client, dealership=car.car_type.dealerships.first(), is_paid=False
#         )
#
#         car_type = car.car_type
#         order_quantity, _ = OrderQuantity.objects.get_or_create(
#             order=order, car_type=car_type
#         )
#         car.block(order)
#         client.order_cart.add(car)


# PUT METHODS


class CarUpdateView(generics.UpdateAPIView, GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
