from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from rest_framework.serializers import Serializer

from account.models import CustomUser
from account.repository import UserRepository


class LoginSerializer(Serializer):
    phone = PhoneNumberField()


class VerifyPhoneSerializer(Serializer):
    confirm_code = serializers.CharField(min_length=4, max_length=4)


class UserSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "phone",
            "used_referral_code",
            "invite_referral_code",
            "referred_users",
        ]

    def get_referred_users(self, user):
        referred_users_phones = UserRepository.get_users_by_referral_code(
            user.invite_referral_code
        )
        return referred_users_phones


class UsedReferralCodeSerializer(Serializer):
    used_referral_code = serializers.CharField(min_length=6, max_length=6)
