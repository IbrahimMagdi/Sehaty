from enum import Enum
from .base_validator import BaseValidator

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class GenderValidator(BaseValidator):
    def __init__(self, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper

    def validate(self):
        try:
            gender = Gender(self.value.lower())
            self.response_status = 200
            self.response_data = gender
        except ValueError:
            self.response_message = f"الجنس يجب أن يكون واحدًا من: {', '.join(g.value for g in Gender)}"
