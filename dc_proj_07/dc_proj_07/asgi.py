"""
ASGI config for dc_proj_07 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

import webapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dc_proj_07.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        webapp.routing.websocket_urlpatterns
    )
})
