from django.core import exceptions
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ...models import User, Profile

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('email', 'password', 'password1')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail': 'passwords does not match'})
        try :
            validate_password(password=attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)




class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({'detail': 'user is not verified'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if not self.user.is_verified:
                raise serializers.ValidationError({'detail': 'user is not verified'})
        validate_data['user_id'] = self.user.id
        validate_data['email'] = self.user.email
        return validate_data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({'detail': 'passwords does not match'})
        try :
            validate_password(password=attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new password': list(e.messages)})
        return super().validate(attrs)

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'email','first_name', 'last_name', 'image', 'description')

class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'user does not exist'})
        if user.is_verified:
            raise serializers.ValidationError({'details':'user is already verified'})
        attrs['user'] = user
        return super().validate(attrs)
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'details':'user does not exist'})
        attrs['user'] = user
        return super().validate(attrs)

class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'details':'passwords does not match'})
        try :
            validate_password(password=attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

