from extension.date import ExtendedDate
from .base_validator import BaseValidator

class BirthDateValidator(BaseValidator):
    def __init__(self, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper

    def validate(self):
        ext_date = ExtendedDate(self.value)
        checks = [
            ext_date.validate_required(self.msg_helper.get("SignUp", "check_birth_date", "none")),
            ext_date.validate_format(self.msg_helper.get("SignUp", "check_birth_date", "Invalid")),
            ext_date.validate_age_range(
                13,
                100,
                under_msg="العمر يجب أن يكون 13 سنة على الأقل",
                over_msg=self.msg_helper.get("SignUp", "check_birth_date", "illogical")
            )
        ]

        for ok, msg in checks:
            if not ok:
                self.response_message = msg
                return

        self.response_status = 200
        self.response_data = ext_date.date