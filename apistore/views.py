from rest_framework.views import APIView

from store.models import Car

from apistore.serializers import CarSerializer


class ApiCars(APIView):
    http_method_names = ["get", "post", "put"]

    def get(self, request):
        ...

    def post(self, request):
        ...

    def put(self, request):
        ...