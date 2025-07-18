# """
# ASGI config for tiktopApi project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiktopApi.settings.base")
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

# application = get_asgi_application()


# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from notifications.routers.routing import websocket_urlpatterns

# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiktopApi.settings.base")
# django.setup()

# application = ProtocolTypeRouter(
#     {
#         "http": django.core.asgi.get_asgi_application(),
#         "websocket": AuthMiddlewareStack(  # Use JWTAuthMiddleware here if using JWT
#             URLRouter(websocket_urlpatterns)
#         ),
#     }
# )
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
# from notifications.routing import websocket_urlpatterns  # you’ll create this file soon
from notifications.routers.routing import websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiktopApi.base")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
