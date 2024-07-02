from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import index, contacts, get_product


app_name = CatalogConfig.name

urlpatterns = [
    path("", index, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>", get_product, name="product"),
]
