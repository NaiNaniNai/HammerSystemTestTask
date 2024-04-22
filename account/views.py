from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from account.serializers import LoginSerializer, VerifyPhoneSerializer
from account.service import LoginService, VerifyPhoneService


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class LoginView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.error_messages)

        service = LoginService(request, serializer)
        data, status = service.post()
        return JsonResponse(data, status=status)


class VerifyPhoneView(APIView):
    def post(self, request, token):
        serializer = VerifyPhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.error_messages)

        service = VerifyPhoneService(request, serializer, token)
        data, status = service.post()
        return JsonResponse(data, status=status)
