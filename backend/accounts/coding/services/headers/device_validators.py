from core.version_controls import systems_controls
from .interfaces import DeviceValidator

class WebsiteValidator(DeviceValidator):
    def is_supported_version(self, version):
        return version in systems_controls['development']['website']

class AndroidValidator(DeviceValidator):
    def is_supported_version(self, version):
        return version in systems_controls['development']['android']

class IOSValidator(DeviceValidator):
    def is_supported_version(self, version):
        return version in systems_controls['development']['ios']