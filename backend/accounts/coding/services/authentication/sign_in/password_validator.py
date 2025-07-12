from ..sign_up.base_validator import BaseValidator
from  extension.string import Extension
from .....models import UserPasswords
from django.contrib.auth import authenticate


class PasswordValidator(BaseValidator):
    def __init__(self, request, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper
        self.request = request

    def validate(self):
        ext_password = Extension(self.value.strip())
        checks = [
            ext_password.validate_required(self.msg_helper.get("SignUp", "check_password", "none")),
            ext_password.validate_min(8, self.msg_helper.get("SignUp", "check_password", "min")),
            ext_password.validate_max(120, self.msg_helper.get("SignUp", "check_password", "max"))
        ]
        for ok, msg in checks:
            if not ok:
                self.response_message = msg
                return

        self.response_status = 200

class PasswordAuthenticator(PasswordValidator):

    def authenticate_user(self, user):
        self.validate()
        st, msg, data = self.get_response()
        if st != 200:
            return st, msg, data
        user_auth = authenticate(username=user.username, password=self.value, backend='django.contrib.auth.backends.ModelBackend')
        if user_auth:
            self.response_status = 200
            return self.response_status, self.response_message, self.response_data
        try:
            pass_old = UserPasswords.objects.get(user=user, password=self.value)
            date_time = pass_old.created_at.strftime("%m/%d/%Y, %I:%M %p")
            self.response_message = f"{self.msg_helper.get('SignIn', 'check_password', 'pass_old')} {date_time}"
            self.response_status = 400

        except UserPasswords.DoesNotExist:
            self.response_message = self.msg_helper.get("SignIn", "check_password", "incorrect")
            self.response_status = 400
        return self.response_status, self.response_message, self.response_data