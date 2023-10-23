from django.urls import path

from store import views

urlpatterns = [
    path("", views.register_client, name="register_client"),
    path("store/", views.redirect_on_store_page, name="redirect_on_store_page"),
    path("add-new-car-type/", views.add_new_car_type, name="add_new_car_type"),
    path("get-all-types/", views.get_all_types_of_cars, name="get_all_types_of_cars"),
]
