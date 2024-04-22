from phonenumber_field.modelfields import PhoneNumberField

from account.models import CustomUser


class UserRepository:
    @staticmethod
    def check_user(phone: PhoneNumberField) -> bool:
        user = CustomUser.objects.filter(phone=phone).first()
        if not user:
            return False
        return user

    @staticmethod
    def create_user(phone: PhoneNumberField) -> None:
        CustomUser.objects.create_user(phone=phone)
