"""
ASGI config for dc_websoc_asyncwebsoc_cons_04 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

import webapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dc_websoc_asyncwebsoc_cons_04.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            webapp.routing.websocket_urlpatterns
        )
    )
})
