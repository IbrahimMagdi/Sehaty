from ..validation_code import ValidationCodeService
from ..sign_in.user_name import UserNameAuthenticator
class CheckAccountValidator(UserNameAuthenticator):

    def check_email(self):
        self.check_user()
        st, msg, data = self.get_response()
        if st != 200:
            return st, msg, None
        call_send_code_email = ValidationCodeService(self.request).send_code_email(data, "resat_pass")
        self.response_status = call_send_code_email[0]
        self.response_message = call_send_code_email[1]
        self.response_data = call_send_code_email[2]

