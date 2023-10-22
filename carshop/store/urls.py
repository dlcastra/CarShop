from django.urls import path

from store import views

urlpatterns = [
    path("", views.register_client, name="register_client"),
    path("store/", views.redirect_on_store_page, name="redirect_on_store_page"),
]
