from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .. import views

urlpatterns = [
    # registration
    path('registration/',views.RegistrationApiView.as_view(),name='registration'),
    # activation
    path('test-email/', views.TestEmailSend.as_view(),name='test-email'),
    # path('activation/confirm/',),
    # path('activation/resend/',),
    # change password
    path('change_password/',views.ChangePasswordApiView.as_view(),name='change-password'),
    # reset password
    # login token
    path('token/login/',views.CustomObtainAuthToken.as_view(),name='token_login'),
    path('token/logout/',views.CustomDiscardAuthToken.as_view(),name='token_logout'),
    # login jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]