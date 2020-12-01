from django.urls import path

from chatbot import views

urlpatterns = [
    path('', views.home, name='chatbot'),
    path('<int:instance_id>/status', views.status_changed, name='on-off'),
    path('<int:instance_id>/input', views.chat, name='input'),
]
