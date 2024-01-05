import rest_framework.authtoken.views
from django.urls import path
from rest_framework import routers

from apistore import views

router = routers.DefaultRouter()
router.register(r"cars-api", views.CarViewSet, "car")
router.register(r"dealers-api", views.DealersViewSet, "dealer")
router.register(r"types-api", views.CarTypeViewSet, "car-type")
router.register(r"create-order", views.CreateOrderView, "buy-car")
router.register(r"cart", views.CartView, "cart")

urlpatterns = router.urls
urlpatterns += [
    path("api-token-auth/", rest_framework.authtoken.views.obtain_auth_token)
]
