from django.urls import path
from .code import *

urlpatterns = [
    path('check-account', check_account_api),
    path('check-code', check_code_api),
    path('new-password', new_password_api),
]

