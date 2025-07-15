from .base_validator import BaseValidator
from .....models import Emails
from ..validation_code import ValidationCodeService
from rest_framework import status
from .email_validator import EmailValidator

class SendEmailValidator(BaseValidator):
    def __init__(self, request, value, msg_helper):
        super().__init__(value, msg_helper.lang)
        self.msg_helper = msg_helper
        self.request = request

    def validate(self):
        try:
            get_email = Emails.objects.get(email=self.value, user=self.request.user, is_credibility=False)
            call_send_code_email = ValidationCodeService(self.request).send_code_email(get_email, "verified")
            self.response_status = call_send_code_email[0]
            self.response_message = call_send_code_email[1]
            self.response_data = {'verification_callback': call_send_code_email[2]}
        except Emails.DoesNotExist:
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.response_message = self.msg_helper.get("SignUp", "check_email", "incorrect")

class ResendEmailValidator:
    def __init__(self, request, email, msg_helper):
        self.request = request
        self.email = email
        self.msg_helper = msg_helper

    def check_email(self):
        def check_email_taken_by_other():
            return Emails.objects.filter(email=self.email).exclude(user=self.request.user).exists()

        check_email = EmailValidator(self.email, self.msg_helper, check_email_taken_by_other)
        check_email.validate()
        st, msg, data = check_email.get_response()
        if st != 200:
            return st, msg, None
        send_email = SendEmailValidator(self.request, self.email, self.msg_helper)
        send_email.validate()
        return send_email.get_response()