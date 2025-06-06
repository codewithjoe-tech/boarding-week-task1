from django.urls import path
from . views import *

urlpatterns = [
    path('register' , RegisterUser.as_view()),
    path('verify-email/<id>' ,VerifyEmail.as_view() ),
    path('login' , Login.as_view()),
    path('refresh' , RefreshView.as_view()),
    path('login-otp' , LoginOtp.as_view()),
    path('verify-otp' , VerifyOTP.as_view()),
    path('logout' , Logout.as_view()),
    path('resend-otp' , ResentOTP.as_view()),
]

