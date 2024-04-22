from django.urls import path
from account.views import LoginView, VerifyPhoneView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("verify/<str:token>", VerifyPhoneView.as_view(), name="verify"),
]
