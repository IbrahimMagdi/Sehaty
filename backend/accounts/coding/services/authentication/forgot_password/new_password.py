from ..sign_up.base_validator import BaseValidator
from ..sign_in.user_name import UserNameAuthenticator
from ..sign_up.password_validator import PasswordValidator
from .....models import CredibilityCodes, UserPasswords
from django.contrib.auth.hashers import check_password
from .tasks import update_password_async

class SecretCodeValidator(BaseValidator):
    def __init__(self, email_obj, value, msg_helper):
        super().__init__(value, msg_helper)
        self.email_obj = email_obj
        self.msg_helper = msg_helper

    def validate(self):
        try:
            code_obj = CredibilityCodes.objects.get(
                email=self.email_obj,
                resat_pass_code=self.value,
                resat_pass=True,
                is_done=False,
                expired=False,
                finished=True
            )
            self.response_status = 200
            self.response_data = self.email_obj.user
        except CredibilityCodes.DoesNotExist:
            self.response_status = 400
            self.response_message = self.msg_helper.get("ForgotPassword", "check_code", "code_is_incorrect")

class CheckUserAndCodeService:
    def __init__(self, request, email, code, msg_helper):
        self.email = email
        self.code = code
        self.msg_helper = msg_helper
        self.request = request

    def check_secret_code(self):
        user_auth = UserNameAuthenticator(self.request, self.email, self.msg_helper)
        user_auth.check_user()
        st, msg, email_obj = user_auth.get_response()
        if st != 200:
            return st, msg, None
        code_validator = SecretCodeValidator(email_obj, self.code, self.msg_helper)
        code_validator.validate()
        return code_validator.get_response()


class CheckPasswordValidator(PasswordValidator):
    def __init__(self, request, value, msg_helper):
        super().__init__(value, msg_helper)
        self.request = request
        self.msg_helper = msg_helper

    def check_new_password(self, email, code):
        check_secret = CheckUserAndCodeService(self.request, email, code, self.msg_helper)
        self.response_status, self.response_message, user_obj = check_secret.check_secret_code()
        if self.response_status != 200:
            return self.response_status, self.response_message, None
        self.validate()
        if self.response_status != 200:
            return self.get_response()
        old_pass = UserPasswords.objects.filter(user=user_obj).first()
        if old_pass and check_password(self.value, old_pass.password):
            self.response_status = 400
            self.response_message = self.msg_helper.get("ForgotPassword", "change_pass", "old_new_equal")
            return self.get_response()
        update_password_async.delay(user_obj.id, self.value, code)
        self.response_status = 200
        self.response_message = self.msg_helper.get("ForgotPassword", "change_pass", "successfully")