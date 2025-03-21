from django.urls import path
from .views import RegisterView, OTPVerifyView, LoginView, UpdateUserView, ForgotPasswordView, UserDetailView,reset_password_page

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('user-profile/', UserDetailView.as_view(), name='user-profile'),
    path('reset-password/<uidb64>/<token>/', reset_password_page, name='reset-password'),
]
