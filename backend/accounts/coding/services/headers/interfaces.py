from abc import ABC, abstractmethod

class DeviceValidator(ABC):
    @abstractmethod
    def is_supported_version(self, version: str) -> bool:
        pass