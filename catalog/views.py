from pathlib import Path

from django.shortcuts import render
import json
from config import settings
from catalog.models import Product

FEEDBACK_FILE_PATH: Path = settings.BASE_DIR.joinpath("feedback.json")


def index(request):
    products_list = Product.objects.all()
    context = {"object_list": products_list}
    return render(request, "catalog/index.html", context)


def get_product(request, pk):
    one_product = Product.objects.get(pk=pk)
    context = {"object": one_product}
    return render(request, "catalog/product.html", context)


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
