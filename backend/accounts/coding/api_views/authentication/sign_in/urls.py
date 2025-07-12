from django.urls import path, include
from .code import *


urlpatterns = [
    path('execute', form_api),
]

