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

    def post(self, request, pk):
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

        return Response(
            {"message": "Car was added to your cart"}, status=status.HTTP_201_CREATED
        )


class CartView(generics.ListAPIView, generics.RetrieveUpdateAPIView, GenericViewSet):
    queryset = Order.objects.filter(is_paid=False)
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = self.get_object()

        if not order.is_paid:
            client = order.client
            cars = Car.objects.filter(blocked_by_order=order)

            for car in cars:
                car.sell()
                car.owner = client
                car.save()

            # create_invoice(order,webhook_url="https://webhook.site/be9e296b-d8f0-48e8-9119-467e57f0e19b",)
            create_invoice(order, reverse("webhook-mono", request=request))
            order.is_paid = True
            order.status = "paid"
            order.save()

            return Response(
                {"invoice": order.invoice_url},
                status=status.HTTP_200_OK,
            )

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        cars = Car.objects.filter(blocked_by_order=order)

        for car in cars:
            car.unblock()
        order.delete()

        return Response({"message": "The order was successfully canceled"})


class MonoAcquiringWebhookReceiver(APIView):
    def post(self, request):
        try:
            verify_signature(request)
        except Exception:
            return Response({"status": "error"}, status=400)
        reference = request.data.get("reference")
        order = Order.objects.get(id=reference)
        if order.order_id != request.data.get("invoiceId"):
            return Response({"status": "error"}, status=400)
        order.status = request.data.get("status", "error")
        order.save()
        return Response({"status": "ok"})
