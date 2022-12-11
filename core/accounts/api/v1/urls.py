from django.urls import path
# from rest_framework.authtoken.views import ObtainAuthToken
from . import views

app_name = 'api-v1'

urlpatterns = [
    # registration
    path('registration/',views.RegistrationApiView.as_view(),name='registration'),
    # change password
    # reset password
    # login token
    path('token/login/',views.CustomObtainAuthToken.as_view(),name='token_login'),
    path('token/logout/',views.CustomDiscardAuthToken.as_view(),name='token_logout'),
    # login jwt
]