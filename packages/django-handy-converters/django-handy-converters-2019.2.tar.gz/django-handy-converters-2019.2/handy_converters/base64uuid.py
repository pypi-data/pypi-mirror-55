import uuid
import base64

from django.urls import register_converter


class Base64UUIDConverter:
    regex = '.{22}'

    @staticmethod
    def decode(value):
        return uuid.UUID(bytes=base64.urlsafe_b64decode(value + '=='))

    @staticmethod
    def encode(value):
        return base64.urlsafe_b64encode(value.bytes).decode().rstrip('==')

    def to_python(self, value):
        return self.decode(value)

    def to_url(self, value):
        return self.encode(value)


register_converter(Base64UUIDConverter, 'base64uuid')
