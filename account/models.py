from typing import List

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager

from account.utils import generate_referral_code


class CustomUserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, phone: str, password=None):
        if not phone:
            raise ValueError("Phone is required!")

        user, _ = CustomUser.objects.get_or_create(phone=phone)

        if user.invite_referral_code is None:
            user.invite_referral_code = generate_referral_code()
            user.save()

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(
            phone=phone,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Model of User"""

    phone = PhoneNumberField(unique=True, verbose_name="Номер телефона")
    used_referral_code = models.CharField(
        max_length=6,
        null=True,
        default=None,
        verbose_name="Реферальный код, по которому пользователь присоединился",
    )
    invite_referral_code = models.CharField(
        max_length=6,
        null=True,
        default=None,
        verbose_name="Реферальный код пользователя для приглашений других",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.phone)
