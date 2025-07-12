from extension.string import Extension
from .base_validator import BaseValidator

class NameValidator(BaseValidator):
    def __init__(self, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper

    def validate(self):
        ext_name = Extension(self.value or "")
        checks = [
            ext_name.validate_required(self.msg_helper.get("SignUp", "check_name", "none")),
            ext_name.validate_min(3, self.msg_helper.get("SignUp", "check_name", "min")),
            ext_name.validate_max(50, self.msg_helper.get("SignUp", "check_name", "max")),
        ]

        for ok, msg in checks:
            if not ok:
                self.response_message = msg
                return

        self.response_status = 200
