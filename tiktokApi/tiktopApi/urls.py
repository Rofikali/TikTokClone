# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('api.urls')),
#     path('api/', include('like.urls')),
#     path('api/', include('comments.urls')),
#     path('api/', include('search.urls')),
#     # path('api/', include('api.urls', namespace='apis')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

# backend/routing.py
from django.urls import re_path
from notifications.consumers.like_consumer import LikeConsumer

websocket_urlpatterns = [
    re_path(r"^ws/likes/$", LikeConsumer.as_asgi()),
]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# DRF Spectacular imports
from drf_spectacular.views import (
    SpectacularAPIView,
    # SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API apps
    # path("api/", include("api.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("like.urls")),
    path("api/", include("comments.urls")),
    path("api/", include("search.urls")),
    path("api/", include("postsapi.urls")),
    # DRF Spectacular schema and docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # path(
    #     "api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    # ),
]

# Static & Media file serving in debug
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
