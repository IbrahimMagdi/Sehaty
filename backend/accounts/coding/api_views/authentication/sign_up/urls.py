from django.urls import path, include
from .code import *


urlpatterns = [
    path('form-create', form_create_api),
    path('resend-code', re_send_code_api),
    path('verify-email', verify_email_api),

]

