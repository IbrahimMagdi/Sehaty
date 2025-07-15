from extension.string import Extension
from .....models import Emails
from .base_validator import BaseValidator

class EmailValidator(BaseValidator):
    def __init__(self, value, msg_helper, custom_check=None):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper
        self.custom_check = custom_check

    def validate(self):
        ext_email = Extension(self.value or "")
        already_exists_check = self.custom_check or (lambda: Emails.objects.filter(email=self.value).exists())
        checks = [
            ext_email.validate_required(self.msg_helper.get("SignUp", "check_email", "none")),
            ext_email.validate_max(50, self.msg_helper.get("SignUp", "check_email", "max")),
            ext_email.validate_email_format(self.msg_helper.get("SignUp", "check_email", "incorrect")),
            ext_email.validate_already_exists(already_exists_check, self.msg_helper.get("SignUp", "check_email", "already_exists")),
        ]
        for ok, msg in checks:
            if not ok:
                self.response_status = 400
                self.response_message = msg
                return
        self.response_status = 200
