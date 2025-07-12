from datetime import datetime, date
from typing import Tuple

class ExtendedDate:
    def __init__(self, date_str: str, fmt: str = "%Y-%m-%d"):
        self.date_str = date_str.strip() if date_str else ""
        self.fmt = fmt
        self.date = None  # يتم ضبطه فقط بعد التحقق

    def validate_required(self, message: str) -> Tuple[bool, str]:
        if not self.date_str:
            return False, message
        return True, ""

    def validate_format(self, message: str) -> Tuple[bool, str]:
        try:
            self.date = datetime.strptime(self.date_str, self.fmt).date()
            return True, ""
        except (ValueError, TypeError):
            return False, message

    def validate_age_range(self, min_age: int, max_age: int, under_msg: str, over_msg: str) -> Tuple[bool, str]:
        if not self.date:
            return False, "تاريخ الميلاد غير مضبوط. تحقق من الصيغة أولًا."

        today = date.today()
        age = today.year - self.date.year - ((today.month, today.day) < (self.date.month, self.date.day))

        if age < min_age:
            return False, under_msg
        if age > max_age:
            return False, over_msg
        return True, ""
