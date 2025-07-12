from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from ....models import UserBrowsers, Emails
from .header_validator import HeaderValidator

class AuthenticationChecker:
    def __init__(self, request, token, language='en'):
        self.request = request
        self.token = token
        self.language = language
        self.now = now()

    def check_authenticated(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return self._not_authenticated_response()

        user = self.request.user

        if not self.request.user or not self.request.user.is_authenticated or not self.request.user.is_active:
            return self._not_authenticated_response()

        try:
            browser = UserBrowsers.objects.get(user=user, token=self.token, website=True, is_done=True, close_pass=False)
        except UserBrowsers.DoesNotExist:
            return status.HTTP_401_UNAUTHORIZED, self._msg("device_recognized"), None

        try:
            email = Emails.objects.get(user=user, is_main=True, is_credibility=False)
        except Emails.DoesNotExist:
            email = None

        if email or user.gender == "":
            return status.HTTP_409_CONFLICT, "", None

        browser.ln = self.language
        browser.save()
        return status.HTTP_200_OK, "", None

    def _msg(self, key):
        from ..headers import re_message as message
        return message.messages['check']['CheckCall']['is_authenticated'][key][self.language]

    def _not_authenticated_response(self):
        if self.request.headers.get('ty') == 'website':
            return status.HTTP_406_NOT_ACCEPTABLE, "", None
        return status.HTTP_400_BAD_REQUEST, self._msg("not_login"), None


class CheckAuthCall:
    def __init__(self, request):
        self.request = request
        self.language = request.META.get("HTTP_LN", "en")
        self.token = request.META.get("HTTP_TK")
        self.response_status, self.response_message, self.response_data = HeaderValidator(request, self.language).validate()

    def is_authenticated(self):
        if self.response_status == 100:
            checker = AuthenticationChecker(self.request, self.token, self.language)
            self.response_status, self.response_message, self.response_data = checker.check_authenticated()
        return self.response_status, self.response_message, self.response_data

    def not_authenticated(self):
        if self.response_status == 100:
            if not self.request.user.is_authenticated:
                self.response_status = status.HTTP_200_OK
            else:
                if self.request.headers.get('ty') == 'website':
                    self.response_status = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    self.response_status = status.HTTP_401_UNAUTHORIZED
        return self.response_status, self.response_message, self.response_data

    def mandatory_sign_out(self):
        try:
            get_item = UserBrowsers.objects.get(token=self.request.headers['tk'], user=self.request.user)
            get_item.is_done = False
            get_item.save()
        except:
            pass
        self.response_message = 'Forced logged out ! '
        if self.request.headers['ty'] == 'website':
            self.response_status = status.HTTP_100_CONTINUE
            response = Response(
                data={"details": 'Forced logged out!'},
                status=401
            )
            self.response_data = response
        else:
            self.response_status = status.HTTP_401_UNAUTHORIZED
        return self.response_status, self.response_message, self.response_data
