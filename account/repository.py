from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from account.models import CustomUser


class UserRepository:
    """ "Class for interacting with the user model"""

    @staticmethod
    def check_user(phone: PhoneNumberField) -> bool:
        user = CustomUser.objects.filter(phone=phone).first()
        if not user:
            return False
        return user

    @staticmethod
    def create_user(phone: PhoneNumberField) -> None:
        CustomUser.objects.create_user(phone=phone)

    @staticmethod
    def get_from_request(request) -> User:
        return request.user

    @staticmethod
    def check_exist_referral_code(referral_code) -> bool:
        user = CustomUser.objects.filter(invite_referral_code=referral_code).first()
        if not user:
            return False
        return True

    @staticmethod
    def get_users_by_referral_code(referral_code):
        phones = list(
            CustomUser.objects.filter(used_referral_code=referral_code).values_list(
                "phone", flat=True
            )
        )
        return [str(phone) for phone in phones]
