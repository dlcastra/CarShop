from rest_framework import routers

from apistore.views import CarViewSet, DealersViewSet, CarTypeViewSet

router = routers.DefaultRouter()
router.register(r"cars-api", CarViewSet, "car")
router.register(r"dealers-api", DealersViewSet, "dealers")
router.register(r"type-api", CarTypeViewSet, "type")

urlpatterns = router.urls
