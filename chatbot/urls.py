from django.urls import path

from chatbot import views

urlpatterns = [
    path('', views.home, name='background'),
    path('bot/', views.bot, name='chatbot'),
]
