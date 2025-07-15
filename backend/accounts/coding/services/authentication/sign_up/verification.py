from .base_validator import BaseValidator
from .....models import Emails, CredibilityCodes
from rest_framework import status
from extension.string import Extension
from .email_validator import EmailValidator

class CheckEmailHandler(BaseValidator):
    def __init__(self, request, email, msg_helper):
        super().__init__(email, msg_helper.lang)
        self.request = request
        self.msg_helper = msg_helper

    def validate(self):
        def check_email_taken_by_other():
            return Emails.objects.filter(email=self.value).exclude(user=self.request.user).exists()

        check_email = EmailValidator(self.value, self.msg_helper, check_email_taken_by_other)
        check_email.validate()
        st, msg, data = check_email.get_response()
        if st != 200:
            return st, msg, None
        try:
            email_obj = Emails.objects.get(email=self.value, user=self.request.user)
            if email_obj.is_credibility:
                self.response_message = self.msg_helper.get("SignUp", "verified", "already_verified")
                self.response_status = 400
            else:
                self.response_status = 200
                self.response_data = email_obj
        except Emails.DoesNotExist:
            self.response_message = self.msg_helper.get("SignUp", "verified", "not_found")
            self.response_status = 404



class CodeFormatValidator(BaseValidator):
    def __init__(self, request, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper
        self.request = request

    def validate(self):
        ext_code = Extension(self.value or "")
        checks = [
            ext_code.validate_required(self.msg_helper.get("SignUp", "verified", "none_code")),
            ext_code.validate_not_equal(6, self.msg_helper.get("SignUp", "verified", "not_equal_code")),
        ]
        for ok, msg in checks:
            if not ok:
                self.response_status = 400
                self.response_message = msg
                return
        self.response_status = 200

class VerifyCodeHandler(BaseValidator):
    def __init__(self, request, email_obj, value, msg_helper):
        super().__init__(value, msg_helper)
        self.request = request
        self.email_obj = email_obj
        self.msg_helper = msg_helper

    def validate(self):
        try:
            code_obj = CredibilityCodes.objects.get(email=self.email_obj, is_done=False, verified=True, code=self.value)
            code_obj.is_done = True
            code_obj.save()
            self.email_obj.is_credibility = True
            self.email_obj.save()
            self.email_obj.user.email_is_credibility = True
            self.email_obj.user.save()
            self.response_status = status.HTTP_200_OK
            self.response_message = self.msg_helper.get("SignUp", "verified", "successfully")
        except CredibilityCodes.DoesNotExist:
            self.response_message = self.msg_helper.get("SignUp", "verified", "Invalid")

class VerifiedEmailValidator(VerifyCodeHandler):

    def check(self):
        check_email = CheckEmailHandler(self.request, self.email_obj, self.msg_helper)
        check_email.validate()
        self.response_status, self.response_message, self.response_data = check_email.get_response()
        if self.response_status != 200:
            return self.response_status, self.response_message, None
        self.email_obj = self.response_data

        check_code = CodeFormatValidator(self.request, self.value, self.msg_helper)
        check_code.validate()
        self.response_status, self.response_message, self.response_data = check_code.get_response()
        if self.response_status != 200:
            return self.response_status, self.response_message, None
        self.validate()
        self.response_status, self.response_message, self.response_data = self.get_response()
        if self.response_status != 200:
            return self.get_response()
