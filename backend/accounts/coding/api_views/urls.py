from django.urls import path, include
from .authentication import urls as urls_authentication


urlpatterns = [
    path('auth/', include(urls_authentication)),
]
