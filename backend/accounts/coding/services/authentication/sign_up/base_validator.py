from abc import ABC, abstractmethod
from rest_framework import status
from backend.accounts.coding.services.authentication import re_message as messages


class BaseValidator(ABC):
    def __init__(self, value, lang="en"):
        self.value = value
        self.lang = lang
        self.response_status = status.HTTP_400_BAD_REQUEST
        self.response_message = ""
        self.response_data = None

    @abstractmethod
    def validate(self):
        pass

    def get_response(self):
        return self.response_status, self.response_message, self.response_data


class MessageHelper:
    def __init__(self, request, section):
        lang = request.META.get("HTTP_LN", "en")
        self.lang = lang if lang in messages.languages else "en"
        self.messages = messages.messages[section]

    def get(self, *keys):
        msg = self.messages
        for key in keys:
            msg = msg[key]
        return msg.get(self.lang)