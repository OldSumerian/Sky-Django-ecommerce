from pathlib import Path
from django.shortcuts import render
import json

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from config import settings
from catalog.models import Product

FEEDBACK_FILE_PATH: Path = settings.BASE_DIR.joinpath("feedback.json")


class CatalogListView(ListView):
    model = Product


class CatalogDetailView(DetailView):
    model = Product


class CatalogCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy("catalog:product_list")



class CatalogUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy("catalog:product_list")


class CatalogDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


def contacts(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "message": request.POST.get("message"),
        }
        print(data)
        # with FEEDBACK_FILE_PATH.open(mode='w', encoding='utf-8') as file:
        #     json.dumps(data, file, indent=2, ensure_ascii=False)

    return render(request, template_name="catalog/contacts.html")
