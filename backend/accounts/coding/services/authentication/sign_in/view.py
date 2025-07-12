from ..sign_up.base_validator import MessageHelper
from .user_name import UserNameAuthenticator
from .password_validator import PasswordAuthenticator
from rest_framework.authtoken.models import Token
from rest_framework import status
import secrets
from django.db import IntegrityError, transaction
from .....models import *

class SignInService:
    def __init__(self, request):
        self.request = request
        self.ln = request.META.get("HTTP_LN", "en")
        self.msg_helper = MessageHelper(request, "authentication")
        self.ty = request.headers.get('ty') or None
        self.tk = request.headers.get('tk') or None
        self.device_info = self.extract_device()

    def extract_device(self):
        return {
            'os': self.request.headers.get('os', '').strip().lower(),
            'device': self.request.headers.get('device', '').strip().lower(),
            'brand': self.request.headers.get('brand', '').strip().lower(),
            'model': self.request.headers.get('model', '').strip().lower(),
            'version': self.request.headers.get('version', '').strip().lower(),
        }

    def generate_unique_token(self, user):
        # 1. تحقق من وجود متصفح مطابق لنفس بيانات الجهاز
        browser_qs = UserBrowsers.objects.filter(
            user=user,
            ln=self.ln,
            type=self.ty,
            website=True,
            is_done=True,
            os=self.device_info.get("os"),
            device=self.device_info.get("device"),
            brand=self.device_info.get("brand"),
            model=self.device_info.get("model"),
            version=self.device_info.get("version"),
        )
        if browser_qs.exists():
            browser = browser_qs.first()
            self.tk = browser.token
            return browser

        # 2. إذا لم يوجد... أنشئ توكن جديد
        max_attempts = 10
        for _ in range(max_attempts):
            token = secrets.token_hex(40)
            try:
                with transaction.atomic():
                    browser = UserBrowsers.objects.create(
                        user=user,
                        token=token,
                        website=True,
                        is_done=True,
                        ln=self.ln,
                        type=self.ty,
                        **self.device_info
                    )
                self.tk = token
                return browser
            except IntegrityError:
                continue
        raise Exception("فشل في توليد token فريد")

    def execute(self):
        user_name = UserNameAuthenticator(self.request, self.request.POST.get("username", "").strip(), self.msg_helper)
        user_name.check_user()
        st, msg, data = user_name.get_response()
        if st != 200:
            return st, msg, None
        password = PasswordAuthenticator(self.request, self.request.POST.get("password", ""), self.msg_helper)
        st, msg, _ = password.authenticate_user(data.user)
        if st != 200:
            return st, msg, None
        try:
            user_token = Token.objects.get(user=data.user)
        except:
            user_token = Token.objects.create(user=data.user)
        self.generate_unique_token(data.user)
        response_status = status.HTTP_200_OK
        response_data = {
            "session": {
                "auth": user_token.key,
                "tk": self.tk,
            },
            "info": {
                "id": str(data.user.id),
                "name": data.user.first_name,
                "gender": data.user.gender,
                "user_type": data.user.user_type,
            },
        }
        return response_status, "", response_data