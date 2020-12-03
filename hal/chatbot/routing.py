from django.urls import re_path

from chatbot import consumers

websocket_urlpatterns = [
    re_path(r'input/$', consumers.MessageConsumer.as_asgi()),
]
