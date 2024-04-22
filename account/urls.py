from django.urls import path
from account.views import LoginView, VerifyPhoneView, LogoutView, ProfileView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("verify/<str:token>", VerifyPhoneView.as_view(), name="verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
