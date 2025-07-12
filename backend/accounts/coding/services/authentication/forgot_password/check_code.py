from ..sign_up.base_validator import BaseValidator
from ..sign_in.user_name import UserNameAuthenticator
from extension.string import Extension
from .....models import CredibilityCodes
import secrets

class CodeValidator(BaseValidator):
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
                self.response_message = msg
                return
        self.response_status = 200

class CheckCodeValidator(UserNameAuthenticator):
    def check_code(self, code):
        self.check_user()
        self.response_status, self.response_message, self.response_data = self.get_response()
        if self.response_status != 200:
            self.get_response()
        email_obj = self.response_data
        validate_code = CodeValidator(self.request, code, self.msg_helper)
        validate_code.validate()
        self.response_status, self.response_message, self.response_data = validate_code.get_response()
        if self.response_status != 200:
           return  validate_code.get_response()
        try:
            code_obj = CredibilityCodes.objects.get(email=email_obj, code=code, resat_pass=True, is_done=False, expired=False, finished=False)
            code_obj.resat_pass_code = f'{secrets.token_hex(30)}'
            code_obj.finished = True
            code_obj.save()
            self.response_status = 200
            self.response_data ={"secrets_code": code_obj.resat_pass_code}
        except CredibilityCodes.DoesNotExist:
            self.response_status = 400
            self.response_message = self.msg_helper.get("ForgotPassword", "check_code", "code_is_incorrect")

