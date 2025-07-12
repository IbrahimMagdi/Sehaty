from celery import shared_task
from django.contrib.auth.hashers import make_password
from .....models import Emails, UserProfile, UserBrowsers, UserPasswords

from ..validation_code import *

@shared_task
def send_code_email_task(email_id, request_data):
    email_obj = Emails.objects.get(id=email_id)
    service = ValidationCodeService(request_data)
    return service.send_code_email(email_obj, "verified")

@shared_task
def create_user_password(user_id, browser_id, password):
    user = UserProfile.objects.get(id=user_id)
    browser = UserBrowsers.objects.get(id=browser_id)
    UserPasswords.objects.create(
        user=user,
        browser=browser,
        password=make_password(password)
    )