from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from account.serializers import (
    LoginSerializer,
    VerifyPhoneSerializer,
    UsedReferralCodeSerializer,
)
from account.service import LoginService, VerifyPhoneService, ProfileService


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class LoginView(CreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.error_messages)

        service = LoginService(request, serializer)
        data, status = service.post()
        return JsonResponse(data, status=status)


class VerifyPhoneView(CreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = VerifyPhoneSerializer

    def create(self, request, token):
        serializer = VerifyPhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.error_messages)

        service = VerifyPhoneService(request, serializer, token)
        data, status = service.post()
        return JsonResponse(data, status=status)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        data = {"Logout": "True"}
        return JsonResponse(data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """Был оставлен APIView из-за проблем с автодокументацией"""

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):
        service = ProfileService(request)
        data, status = service.get()
        return JsonResponse(data, status=status)

    def post(self, request):
        serializer = UsedReferralCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.error_messages)

        service = ProfileService(request)
        data, status = service.post(serializer)
        return JsonResponse(data, status=status)
