from django.shortcuts import render


def home(request):
    return render(request, 'chatbot/HAL.html')


def status_changed(request, instance_id):
    print(request, instance_id)


def chat(request, instance_id):
    print(request, instance_id)
