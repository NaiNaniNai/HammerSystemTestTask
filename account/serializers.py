from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from rest_framework.serializers import Serializer


class LoginSerializer(Serializer):
    phone = PhoneNumberField()


class VerifyPhoneSerializer(Serializer):
    confirm_code = serializers.CharField(min_length=4, max_length=4)
