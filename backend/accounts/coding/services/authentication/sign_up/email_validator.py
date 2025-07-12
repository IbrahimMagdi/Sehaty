from extension.string import Extension
from .....models import Emails
from .base_validator import BaseValidator

class EmailValidator(BaseValidator):
    def __init__(self, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper

    def validate(self):
        ext_email = Extension(self.value or "")
        checks = [
            ext_email.validate_required(self.msg_helper.get("SignUp", "check_email", "none")),
            ext_email.validate_max(50, self.msg_helper.get("SignUp", "check_email", "max")),
            ext_email.validate_email_format(self.msg_helper.get("SignUp", "check_email", "incorrect")),
        ]

        for ok, msg in checks:
            if not ok:
                self.response_message = msg
                return

        if Emails.objects.filter(email=self.value).exists():
            self.response_message = self.msg_helper.get("SignUp", "check_email", "already_exists")
        else:
            self.response_status = 200
