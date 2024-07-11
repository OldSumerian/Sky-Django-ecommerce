from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import CatalogListView, CatalogDetailView, CatalogCreateView, CatalogUpdateView, \
    CatalogDeleteView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path("", CatalogListView.as_view(), name="product_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>", CatalogDetailView.as_view(), name="product_detail"),
    path("product/create", CatalogCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", CatalogUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", CatalogDeleteView.as_view(), name="product_delete"),
]
