from extension.string import Extension
from .base_validator import BaseValidator

class PasswordValidator(BaseValidator):
    def __init__(self, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper

    def validate(self):
        ext_password = Extension(self.value.strip())
        checks = [
            ext_password.validate_required(self.msg_helper.get("SignUp", "check_password", "none")),
            ext_password.validate_min(8, self.msg_helper.get("SignUp", "check_password", "min")),
            ext_password.validate_max(120, self.msg_helper.get("SignUp", "check_password", "max")),
            ext_password.validate_password_strength({
                "lowercase": self.msg_helper.get("SignUp", "check_password", "lowercase"),
                "capital": self.msg_helper.get("SignUp", "check_password", "capital"),
                "number": self.msg_helper.get("SignUp", "check_password", "number"),
                "special": self.msg_helper.get("SignUp", "check_password", "special"),
                "arabic": self.msg_helper.get("SignUp", "check_password", "arabic"),
                "tashkeel": self.msg_helper.get("SignUp", "check_password", "tashkeel"),
                "space": self.msg_helper.get("SignUp", "check_password", "space"),
            })
        ]
        for ok, msg in checks:
            if not ok:
                self.response_status = 400
                self.response_message = msg
                return

        self.response_status = 200