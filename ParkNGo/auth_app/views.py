from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer
from .models import User
from .utility import signup_email
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import EmailOTPVerifySerializer,ResendOTPSerializer,LoginSerializer
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
# from django.shortcuts import get_object_or_404




class UserSignupView(APIView):
    """
    {
     "first_name": "Robil",
     "last_name": "DL",
     "email": "robil@example.com",
     "password": "StrongPass123!",
     "confirm_password": "StrongPass123!",
    "phone": "9876543210",
    "address": "Kochi, Kerala"
    }
    """
    def post(self, request):
        message = False
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
              message = signup_email(user.id)
            if not message:
                 return Response({
                "message": "User registered successfully, Email verification is failed",
                "user": {
                    "id": user.id,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
            if message:
              return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailOTPVerifyView(APIView):
    """
        {
       "email": "robil@example.com",
      "otp": 5632
         }
    """
    def post(self, request):
        serializer = EmailOTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data["user"]
        user.is_verify = True
        user.otp = None  
        user.save()

        return Response(
            {
                "message": "Email verified successfully. Your account is now active.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class ResendOTPLView(APIView):
    """
    {
      "email": "robil@example.com"
      }
    """
    def post(self,request):
        message = False
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            print("enter")
            user = serializer.validated_data["user"]
            message = signup_email(user.id)
        if not message:
            return Response({"message":"not valid email"}, status=status.HTTP_400_BAD_REQUEST)
        if message:
            return Response(
            {
                "message": "OTP generated",
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    """
    POST /api/login/
    Request JSON:
        { "email": "user@example.com", "password": "secret" }

    Response JSON (cookie method):
        { "access": "<access_token>", "user": { id, email, ... } }
    or (json method):
        { "access": "...", "refresh": "...", "user": {...} }
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]

        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": getattr(user, "first_name", ""),
            "last_name": getattr(user, "last_name", ""),
        }

        response = Response(
            {"access": access, "user": user_data},
            status=status.HTTP_200_OK
        )
        expires = timezone.now() + timedelta(seconds=getattr(settings, "SIMPLE_JWT", {}).get("REFRESH_TOKEN_LIFETIME", timedelta(days=7)).total_seconds())
        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIE_NAME,
            value=refresh,
            httponly=settings.REFRESH_TOKEN_COOKIE_HTTPONLY,
            secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
            samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
            path=settings.REFRESH_TOKEN_COOKIE_PATH,
            # max_age=REFRESH_TOKEN_COOKIE_AGE,
            expires=expires
        )

        return response
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)
        if not refresh_token:
            return Response({"detail": "No refresh token present."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist() 
        except Exception:
            pass

        response = Response({"detail": "Logged out."}, status=200)
        response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME, path=settings.REFRESH_TOKEN_COOKIE_PATH)
        return response
