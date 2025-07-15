from typing import Tuple
from enum import Enum
from .regex_patterns import RegexPatterns
class PasswordCondition(Enum):
    LOWERCASE = "lowercase"
    CAPITAL = "capital"
    NUMBER = "number"
    SPECIAL = "special"
    ARABIC = "arabic"
    CONTAINS_FORMATION = "contains_formation"
    SPACE = "space"

class Extension(str):
    def validate_required(self, message: str):
        if not self.strip():
            return False, message
        return True, ""

    def validate_min(self, min_length: int, message: str):
        if len(self.strip()) < min_length:
            return False, message
        return True, ""

    def validate_not_equal(self, equal_length: int, message: str):
        if len(self.strip()) != equal_length:
            return False, message
        return True, ""

    def validate_max(self, max_length: int, message: str):
        if len(self.strip()) > max_length:
            return False, message
        return True, ""

    def validate_email_format(self, message: str):
        if not RegexPatterns.match_email(self.strip()):
            return False, message
        return True, ""

    def validate_password_strength(self, messages: dict) -> Tuple[bool, str]:
        password = self.strip()
        conditions = [
            (PasswordCondition.LOWERCASE, lambda p: any(c.islower() for c in p)),
            (PasswordCondition.CAPITAL, lambda p: any(c.isupper() for c in p)),
            (PasswordCondition.NUMBER, lambda p: any(c.isdigit() for c in p)),
            (PasswordCondition.SPECIAL, lambda p: any(c in '@$!%*?&' for c in p)),
            (PasswordCondition.ARABIC, lambda p: not RegexPatterns.contains_arabic(p)),
            (PasswordCondition.CONTAINS_FORMATION, lambda p: not RegexPatterns.contains_formation(p)),
            (PasswordCondition.SPACE, lambda p: " " not in p),
        ]
        for key, check in conditions:
            if not check(password):
                match key:
                    case PasswordCondition.LOWERCASE:
                        return False, messages["lowercase"]
                    case PasswordCondition.CAPITAL:
                        return False, messages["capital"]
                    case PasswordCondition.NUMBER:
                        return False, messages["number"]
                    case PasswordCondition.SPECIAL:
                        return False, messages["special"]
                    case PasswordCondition.ARABIC:
                        return False, messages["arabic"]
                    case PasswordCondition.CONTAINS_FORMATION:
                        return False, messages["contains_formation"]
                    case PasswordCondition.SPACE:
                        return False, messages["space"]
        return True, ""

    def validate_choices(self, choices: list, message: str):
        if self.strip().lower() not in [c.lower() for c in choices]:
            return False, message
        return True, ""

    @staticmethod
    def validate_already_exists(exists_func ,message: str):
        if exists_func():
            return False, message
        return True, ""
