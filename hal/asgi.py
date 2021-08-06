"""
ASGI config for hal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from dotenv import load_dotenv

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import django

from chatbot import routing

load_dotenv()
load_dotenv('/var/local/db_credentials.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hal.settings')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

django.setup()


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns,
        )
    )})
