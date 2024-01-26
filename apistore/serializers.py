from rest_framework import serializers

from store.models import Car, CarType, Dealership, Order


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = ["id", "name", "brand", "price"]


class DealershipSerializer(serializers.ModelSerializer):
    # available_car_types = serializers.PrimaryKeyRelatedField(queryset=CarType.objects.all(),many=True)

    class Meta:
        model = Dealership
        fields = ["id", "name", "available_car_types"]


class CarSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            "id",
            "car_type",
            "color",
            "year",
            "image",
            "price",
        ]

    def get_price(self, obj):
        car_type = obj.car_type
        if car_type:
            return car_type.price
        return None


class OrderSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "client", "dealership", "is_paid", "cars"]
