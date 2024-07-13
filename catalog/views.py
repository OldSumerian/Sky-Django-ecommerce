from pathlib import Path
from django.shortcuts import render
import json

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from config import settings
from catalog.models import Product

FEEDBACK_FILE_PATH: Path = settings.BASE_DIR.joinpath("feedback.json")


class CatalogListView(ListView):
    model = Product


class CatalogDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object



class CatalogCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy("catalog:product_list")



class CatalogUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse(viewname="catalog:product_detail", kwargs={"pk": self.object.pk})


class CatalogDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"
    context_object_name = "contacts"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["contacts"] = json.loads(FEEDBACK_FILE_PATH.read_text(encoding='utf-8'))
        return context

