import rest_framework.authtoken.views
from django.urls import path
from rest_framework import routers

from apistore import views

router = routers.DefaultRouter()
router.register(r"cars-api", views.CarViewSet, "car")
router.register(r"cars-api", views.CarUpdateView, "update-car")
# router.register(r"cars-api", views.BuyCarView, "car")
router.register(r"dealers-api", views.DealersViewSet)
router.register(r"type-api", views.CarTypeViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("api-token-auth/", rest_framework.authtoken.views.obtain_auth_token)
]
