from django.urls import path
from .views import RegisterView, OTPVerifyView, LoginView, ForgotPasswordView, reset_password_page, GetAccessToken

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', reset_password_page, name='reset-password'),
    path('get-access-token/', GetAccessToken.as_view(), name='get-access-token'),
]
