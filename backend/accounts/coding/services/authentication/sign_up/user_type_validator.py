from enum import Enum
from .base_validator import BaseValidator

class UserType(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"
    CLINIC_ADMIN = "clinic_admin"

class UserTypeValidator(BaseValidator):
    def __init__(self, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper

    def validate(self):
        try:
            user_type = UserType(self.value.lower())
            self.response_status = 200
            self.response_data = user_type
        except ValueError:
            self.response_message = f"نوع المستخدم يجب أن يكون واحدًا من: {', '.join(t.value for t in UserType)}"
