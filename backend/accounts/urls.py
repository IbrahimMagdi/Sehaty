from django.urls import path, include
from .coding import urls as urls_coding


urlpatterns = [
    path('', include(urls_coding)),

]
