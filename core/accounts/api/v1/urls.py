from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import views

app_name = 'api-v1'

urlpatterns = [
    # registration
    path('registration/',views.RegistrationApiView.as_view(),name='registration'),
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
    # profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
]