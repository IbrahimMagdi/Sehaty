from rest_framework import status
from ..headers import re_message as message

class HeaderValidator:
    SUPPORTED_DEVICES = {
        'website': 'WebsiteValidator',
        'android': 'AndroidValidator',
        'ios': 'IOSValidator',
    }

    def __init__(self, request, language='en'):
        self.request = request
        self.language = language if language in message.languages else "en"

    def validate(self):
        device = self.request.META.get('HTTP_TY')
        version = self.request.META.get('HTTP_VC', "0.0.0")

        if device not in self.SUPPORTED_DEVICES:
            return status.HTTP_409_CONFLICT, message.messages['check']['CheckCall']['check_headers']['not_access'][self.language], None

        from .device_validators import WebsiteValidator, AndroidValidator, IOSValidator
        validator_map = {
            'website': WebsiteValidator(),
            'android': AndroidValidator(),
            'ios': IOSValidator(),
        }

        validator = validator_map.get(device)
        if validator and validator.is_supported_version(version):
            return status.HTTP_100_CONTINUE, "", None
        else:
            return status.HTTP_428_PRECONDITION_REQUIRED, message.messages['check']['CheckCall']['check_headers']['update_app'][self.language], None
