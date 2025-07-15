from .base_validator import MessageHelper
from .name_validator import NameValidator
from .email_validator import EmailValidator
from .birth_date_validator import BirthDateValidator
from .password_validator import PasswordValidator
from .gender_validator import GenderValidator
from .user_type_validator import UserTypeValidator
from .resend_code import ResendEmailValidator
from .verification import VerifiedEmailValidator
from .....models import *
from ..validation_code import *
from .tasks import send_code_email_task, create_user_password

from rest_framework.authtoken.models import Token
import secrets, string
from django.db import IntegrityError, transaction


class SignUpService:
    def __init__(self, request):
        self.request = request
        self.ln = request.META.get("HTTP_LN", "en")
        self.msg_helper = MessageHelper(request, "authentication")
        self.ty = request.headers.get('ty') or None
        self.tk = request.headers.get('tk') or None
        self.device_info = self.extract_device()
        self.name = self.email = self.password = None
        self.gender = self.user_type = self.birth_date = None

    def extract_device(self):
        return {
            'os': self.request.headers.get('os', '').strip().lower(),
            'device': self.request.headers.get('device', '').strip().lower(),
            'brand': self.request.headers.get('brand', '').strip().lower(),
            'model': self.request.headers.get('model', '').strip().lower(),
            'version': self.request.headers.get('version', '').strip().lower(),
        }

    def validate_all(self):
        name_val = NameValidator(self.request.POST.get("name", "").strip(), self.msg_helper)
        name_val.validate()
        st, msg, _ = name_val.get_response()
        if st != 200:
            return st, msg
        self.name = name_val.value

        email_val = EmailValidator(self.request.POST.get("email", "").strip(), self.msg_helper)
        email_val.validate()
        st, msg, _ = email_val.get_response()
        if st != 200:
            return st, msg
        self.email = email_val.value

        birth_val = BirthDateValidator(self.request.POST.get("birth_date", "").strip(), self.msg_helper)
        birth_val.validate()
        st, msg, date = birth_val.get_response()
        if st != 200:
            return st, msg
        self.birth_date = date

        pass_val = PasswordValidator(self.request.POST.get("password", ""), self.msg_helper)
        pass_val.validate()
        st, msg, _ = pass_val.get_response()
        if st != 200:
            return st, msg
        self.password = pass_val.value

        type_val = UserTypeValidator(self.request.POST.get("type", "").strip(), self.msg_helper)
        type_val.validate()
        st, msg, tdata = type_val.get_response()
        if st != 200:
            return st, msg
        self.user_type = tdata.value

        gender_val = GenderValidator(self.request.POST.get("gender", "").strip(), self.msg_helper)
        gender_val.validate()
        st, msg, gdata = gender_val.get_response()
        if st != 200:
            return st, msg
        self.gender = gdata.value

        return status.HTTP_200_OK, ""

    @staticmethod
    def generate_username():
        characters = string.ascii_lowercase + string.digits
        for _ in range(20):
            candidate = ''.join(secrets.choice(characters) for _ in range(16))
            if not UserProfile.objects.filter(username=candidate).exists():
                return candidate
        raise Exception("فشل في توليد اسم مستخدم فريد")

    def create_user_account(self):
        return UserProfile.objects.create_user(
            username=self.generate_username(),
            first_name=self.name,
            email=self.email,
            password=self.password,
            user_type=self.user_type,
            gender=self.gender,
            birth_date=self.birth_date,
        )

    def generate_unique_token(self, user):
        max_attempts = 10
        for _ in range(max_attempts):
            token = secrets.token_hex(40)
            try:
                with transaction.atomic():
                    browser, created = UserBrowsers.objects.get_or_create(
                        user=user,
                        token=token,
                        website=True,
                        defaults={
                            'is_done': True,
                            'ln': self.ln,
                            'type': self.ty,
                            **self.device_info
                        }
                    )
                if not created:
                    updated = False
                    if browser.ln != self.ln:
                        browser.ln = self.ln
                        updated = True
                    if not browser.is_done:
                        browser.is_done = True
                        updated = True
                    for k, v in self.device_info.items():
                        if getattr(browser, k, None) != v:
                            setattr(browser, k, v)
                            updated = True
                    if updated:
                        browser.save()
                self.tk = token
                return browser
            except IntegrityError:
                continue
        raise Exception("فشل في توليد token فريد")

    def execute(self):
        st, msg = self.validate_all()
        if st != 200:
            return st, msg, None
        user = self.create_user_account()
        auth_token = Token.objects.create(user=user)
        email_obj = Emails.objects.create(user=user, email=self.email, is_main=True)
        browser = self.generate_unique_token(user)
        create_user_password.delay(user.id, browser.id, self.password)
        send_code_email_task.delay(email_obj.id, {"user_id": user.id})
        response_status = status.HTTP_201_CREATED
        response_data = {
            "session": {
                "auth": auth_token.key,
                "tk": self.tk,
            },
            "info": {
                "id": str(user.id),
                "name": user.first_name,
                "gender": user.gender,
                "user_type": user.user_type,
            },
        }
        return response_status, "", response_data


    def resend_code(self):
        type_val = ResendEmailValidator(self.request, self.request.POST.get("email", "").strip(), self.msg_helper)
        return type_val.check_email()


    def verify_email(self):
        email_value = self.request.POST.get("email", "").strip()
        code = self.request.POST.get("code", "").strip()
        check_verified = VerifiedEmailValidator(self.request, email_value, code, self.msg_helper)
        check_verified.check()
        return check_verified.get_response()

