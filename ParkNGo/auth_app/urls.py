from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView 

from . import views
urlpatterns = [
    path("v1/auth_reg/",views.UserSignupView.as_view(),name="auth_reg"),
    path("v1/sign_up_otp/",views.EmailOTPVerifyView.as_view(),name="sign_up_otp"),
    path("v1/resend_otp/",views.ResendOTPLView.as_view(),name="resend_otp"),
    path("v1/login/",views.LoginView.as_view(), name="api_login"),
    path("v1/logout/", views.LogoutView.as_view(), name="api_logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] 

