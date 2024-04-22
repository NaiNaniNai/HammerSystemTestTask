import uuid
from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from rest_framework import status

from account.repository import UserRepository

from account.utils import generate_confirm_code
from .task import send_sms_code


class LoginService:
    """Service for login"""

    def __init__(self, request, serializer):
        self.request = request
        self.serializer = serializer

    def post(self) -> tuple:
        token = self._get_token()
        phone = self.serializer.data.get("phone")
        confirm_code = generate_confirm_code()
        print(confirm_code)
        confirm_link = self._get_confirm_link(token)
        self._caching(token, phone, confirm_code)
        send_sms_code.delay()

        return (
            {
                "user": self.serializer.data,
                "next_page": confirm_link,
            },
            status.HTTP_200_OK,
        )

    def _get_confirm_link(self, token) -> str:
        current_site = get_current_site(self.request)
        return f"http://{current_site.domain}/api/verify/{token}"

    def _caching(self, token, phone, confirm_code) -> None:
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        value = {"phone": phone, "confirm_code": confirm_code}
        cache.set(redis_key, value, timeout=settings.USER_CONFIRMATION_TIMEOUT)

    def _get_token(self) -> str:
        token = uuid.uuid4().hex

        return token


class VerifyPhoneService:
    """Service for verify phone"""

    def __init__(self, request, serializer, token):
        self.request = request
        self.serializer = serializer
        self.token = token

    def post(self) -> tuple:
        confirm_code = self.serializer.data.get("confirm_code")
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=self.token)
        user_info = cache.get(redis_key)

        if not user_info:
            return ({"error": "Время действия истекло"}, status.HTTP_400_BAD_REQUEST)

        sent_confirm_code = user_info.get("confirm_code")
        phone = user_info.get("phone")

        if confirm_code != sent_confirm_code:
            return (
                {"error": "Неверный код подтверждения"},
                status.HTTP_400_BAD_REQUEST,
            )

        user = UserRepository.check_user(phone)
        if not user:
            UserRepository.create_user(phone)

        user = UserRepository.check_user(phone)

        login(self.request, user)
        cache.delete(redis_key)

        return ({"message": "Вы авторизовались"}, status.HTTP_200_OK)
