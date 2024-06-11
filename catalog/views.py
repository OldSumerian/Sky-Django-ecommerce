from django.shortcuts import render
import json


def index(request):
    return render(request, template_name='index.html')


def contacts(request):
    if request.method == 'POST':
        data = {'name': request.POST.get('name'), 'phone': request.POST.get('phone'),
                'message': request.POST.get('message')}
        # with open('../user_contacts.json', 'w', encoding='utf-8') as file:
        #     json.dump(data, file)

    return render(request, template_name='contacts.html')

