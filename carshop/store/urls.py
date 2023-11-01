from django.urls import path

from store import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("registration/", views.register_client, name="register_client"),
    path("store/", views.redirect_on_store_page, name="redirect_on_store_page"),
    # ADD
    path(
        "for-staff-only/add-new-car-type/",
        views.add_new_car_type,
        name="add_new_car_type",
    ),
    path("for-staff-only/add-new-car/", views.add_new_car, name="add_new_car"),
    path("for-staff-only/add-dealer/", views.add_dealership, name="add_dealership"),
    # GET
    path(
        "for-staff-only/get-all-types/",
        views.get_all_types_of_cars,
        name="get_all_types_of_cars",
    ),
    path("for-staff-only/get-all-cars/", views.get_all_cars, name="get_all_cars"),
    path(
        "for-staff-only/get-all-dealers/",
        views.get_all_dealership,
        name="get_all_dealership",
    ),
]
