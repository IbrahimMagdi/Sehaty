from django.urls import path, include
from .api_views import urls as urls_api


urlpatterns = [
    path('api/', include(urls_api)),

]