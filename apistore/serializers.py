from rest_framework import serializers

from store.models import Car, CarType, Dealership


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ["name", "brand", "price"]


class DealershipSerializer(serializers.ModelSerializer):
    available_car_types = CarTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Dealership
        fields = ["name", "available_car_types"]


class CarSerializer(serializers.ModelSerializer):
    car_type = CarTypeSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ["id", "color", "year", "image", "car_type"]
