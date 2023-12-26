# from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from store.models import Car, Dealership, CarType

from apistore.serializers import CarSerializer, DealershipSerializer, CarTypeSerializer


# GET AND POST METHODS


class CarTypeViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer

    def get(self, request):
        return Response(self.serializer_class.data, status=status.HTTP_200_OK)


class CarViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Car.objects.filter(owner__isnull=True, blocked_by_order__isnull=True)
    serializer_class = CarSerializer

    def get(self, request):
        return Response(self.serializer_class.data, status=status.HTTP_200_OK)


class DealersViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer

    def get(self, request):
        return Response(self.serializer_class.data, status=status.HTTP_200_OK)


# PUT METHODS
