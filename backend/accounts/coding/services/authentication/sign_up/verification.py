from .base_validator import BaseValidator
from .....models import Emails, CredibilityCodes
from ..validation_code import ValidationCodeService
from rest_framework import status
from extension.string import Extension

class ResendEmailValidator(BaseValidator):
    def __init__(self, request, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper
        self.request = request

    def validate(self):
        try:
            get_email = Emails.objects.get(email=self.value, user=self.request.user, is_credibility=False)
        except Emails.DoesNotExist:
            get_email = None

        if get_email:
            call_send_code_email = ValidationCodeService(self.request).send_code_email(get_email, "verified")
            self.response_status = call_send_code_email[0]
            self.response_message = call_send_code_email[1]
            self.response_data = {
                'verification_callback': call_send_code_email[2],
            }
        else:
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.response_message = self.msg_helper.get("SignUp", "check_email", "incorrect")

class VerifiedEmailValidator(BaseValidator):
    def __init__(self, request, value, email_value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper
        self.request = request
        self.email_value = email_value

    def validate(self):
        ext_code = Extension(self.value or "")
        checks = [
            ext_code.validate_required(self.msg_helper.get("SignUp", "verified", "none_code")),
            ext_code.validate_not_equal(6, self.msg_helper.get("SignUp", "verified", "not_equal_code")),
        ]
        error = next(((ok, msg) for ok, msg in checks if not ok), None)
        return error

    def check_email(self):
        try:
            email_obj = Emails.objects.get(email=self.email_value, user=self.request.user)
        except Emails.DoesNotExist:
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.response_message = self.msg_helper.get("SignUp", "verified", "not_found")
            return

        if email_obj.is_credibility:
            self.response_message = self.msg_helper.get("SignUp", "verified", "already_verified")
            return

        error = self.validate()
        if error:
            self.response_message = error[1]
            return

        try:
            code_obj = CredibilityCodes.objects.get(email=email_obj, is_done=False, code=self.value)
        except CredibilityCodes.DoesNotExist:
            self.response_message = self.msg_helper.get("SignUp", "verified", "Invalid")
            return

        code_obj.is_done = True
        code_obj.save()
        email_obj.is_credibility = True
        email_obj.save()
        email_obj.user.email_is_credibility = True
        email_obj.user.save()
        self.response_status = status.HTTP_200_OK
        self.response_message = self.msg_helper.get("SignUp", "verified", "successfully")
