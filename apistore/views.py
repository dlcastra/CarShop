import requests
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apistore.invoices import create_invoice, verify_signature
from apistore.serializers import (
    CarSerializer,
    DealershipSerializer,
    CarTypeSerializer,
    OrderSerializer,
)
from carshop import settings
from store.models import Car, Dealership, CarType, Client, Order, OrderQuantity


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
    generics.CreateAPIView,
    GenericViewSet,
):
    queryset = Car.objects.filter(owner__isnull=True, blocked_by_order__isnull=True)
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class CreateOrderView(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    GenericViewSet,
):
    queryset = Car.objects.filter(owner__isnull=True, blocked_by_order__isnull=True)
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def post(request, pk):
        car = get_object_or_404(Car, pk=pk)
        if car.blocked_by_order or car.owner:
            return Response(
                {"error": "Car is blocked or already owned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        return Response({"message": "Cars added to the cart"}, status=status.HTTP_201_CREATED)


class CartView(generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    queryset = Order.objects.filter(is_paid=False)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order_info = (
            "https://api.monobank.ua/api/merchant/invoice/status?invoiceId="
        )
        headers = {"X-Token": settings.MONOBANK_TOKEN}
        status_check = order_info + order.order_id
        response = requests.get(status_check, headers=headers)
        data = response.json()

        if not order.is_paid and order.status != "created":
            client = order.client
            cars = Car.objects.filter(blocked_by_order=order)

            for car in cars:
                car.sell()
                car.owner = client
                car.save()

            create_invoice(order, reverse("webhook-mono", request=request))
            return Response(
                {"invoice": order.invoice_url, "message": "Your invoice"},
                status=status.HTTP_200_OK,
            )

        if order.status == "created" and data["status"] == "success":
            if data["status"] == "success":
                order.is_paid = True
                order.status = "paid"
                order.save()
                client = Client.objects.first()
                client.order_cart.clear()
                return Response({"message": "Order was successfully paid"})

        elif data["status"] == "created":
            return Response(
                {
                    "message": "You have not paid for your order yet",
                    "invoice": order.invoice_url,
                }
            )

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        cars = Car.objects.filter(blocked_by_order=order)

        for car in cars:
            car.unblock()
        order.delete()

        return Response({"message": "The order was successfully canceled"})


class MonoAcquiringWebhookReceiver(APIView):

    @staticmethod
    def post(request):
        try:
            verify_signature(request)
        except Exception:
            return Response({"status": "error"}, status=400)
        reference = request.data.get("reference")
        order = Order.objects.get(id=reference)
        if order.invoice_id != request.data.get("invoiceId"):
            return Response({"status": "error"}, status=400)
        order.status = request.data.get("status", "error")
        order.save()
        if order.status == "success":
            order.is_paid = True
            order.save()
            return Response({"status": "Paid"}, status=200)
        return Response({"status": "ok"})
