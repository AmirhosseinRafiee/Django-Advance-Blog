from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
)
from mail_templated import EmailMessage
from datetime import timedelta
from .serializers import (
    RegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    CustomAuthTokenSerializer,
    ActivationResendSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from ..utils import EmailThread
from ...models import Profile

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user = get_object_or_404(User, email=email)
            jwt_access_token = self.get_access_token_for_user(user)
            email_obj = EmailMessage(
                "email/activation-confirm.tpl",
                {"token": jwt_access_token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=10))
        return str(access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        self.email = "admin@admin.com"
        user = get_object_or_404(User, email=self.email)
        jwt_access_token = self.get_access_token_for_user(user)
        email_object = EmailMessage(
            "email/hello.tpl",
            {"token": jwt_access_token},
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_object).start()
        return Response("email sent")

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationConfirmApiView(APIView):
    def post(self, request, token, *args, **kwargs):
        try:
            decode_payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = get_object_or_404(User, id=decode_payload["user_id"])
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (InvalidSignatureError, DecodeError):
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.is_verified:
            return Response(
                {"details": "your account has already been verified"}
            )
        user.is_verified = True
        user.save()
        return Response(
            {
                "details": "your account have been verified and activated successfully"
            }
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_access_token_for_user(user)
        email_obj = EmailMessage(
            "email/activation-confirm.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=10))
        return str(access_token)


class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        jwt_access_token = self.get_access_token_for_user(user)
        email_object = EmailMessage(
            "email/reset-password.tpl",
            {"token": jwt_access_token},
            "admin@admin.com",
            to=[user.email],
        )
        EmailThread(email_object).start()
        return Response(
            {"details": "reset password send successfully"},
            status=status.HTTP_200_OK,
        )

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=10))
        return str(access_token)


class ResetPasswordConfirmApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            decode_payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (InvalidSignatureError, DecodeError):
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, id=decode_payload["user_id"])
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response(
            {"details": "password has been changed successfully"},
            status=status.HTTP_200_OK,
        )
