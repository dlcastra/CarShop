from django.urls import path

from store import views

urlpatterns = [
    path("", views.redirect_on_store_page, name="redirect_on_store_page"),
    path("create_order/<int:pk>/", views.create_order, name="create_order"),
    path("cart/", views.view_cart, name="view_cart"),
    path("pay_order/<int:pk>", views.pay_order, name="pay_order"),
    path("cancel_order/<int:pk>", views.cancel_order, name="cancel_order"),
    # ADD
    path("registration/", views.register_client, name="register_client"),
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
