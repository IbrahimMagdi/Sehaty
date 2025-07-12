from ..sign_up.base_validator import MessageHelper
from .check_account import CheckAccountValidator
from .check_code import CheckCodeValidator
from .new_password import CheckPasswordValidator

class ForgotPasswordService:
    def __init__(self, request):
        self.request = request
        self.ln = request.META.get("HTTP_LN", "en")
        self.msg_helper = MessageHelper(request, "authentication")

    def check_account(self):
        check = CheckAccountValidator(self.request, self.request.POST.get("username", "").strip(), self.msg_helper)
        check.check_email()
        response_status, response_message, response_data = check.get_response()
        return response_status, response_message, response_data

    def check_code(self):
        check = CheckCodeValidator(self.request, self.request.POST.get("username", "").strip(), self.msg_helper)
        check.check_code(self.request.POST.get("secret_code", "").strip())
        response_status, response_message, response_data = check.get_response()
        return response_status, response_message, response_data

    def new_password(self):
        check = CheckPasswordValidator(self.request, self.request.POST.get("new_password", "").strip(), self.msg_helper)
        check.check_new_password(self.request.POST.get("username", "").strip(), self.request.POST.get("secret_code", "").strip())
        response_status, response_message, response_data = check.get_response()
        return response_status, response_message, response_data