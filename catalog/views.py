from pathlib import Path

from django.shortcuts import render
import json
from config import settings


FEEDBACK_FILE_PATH: Path = settings.BASE_DIR.joinpath("feedback.json")


def index(request):
    return render(request, template_name="index.html")


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

    return render(request, template_name="contacts.html")
