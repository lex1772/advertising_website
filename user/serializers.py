from djoser.conf import settings
from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,
    TokenCreateSerializer)
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from user.models import User


# Сериализатор для регистрации пользователя
class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'email', 'first_name',
            'last_name', 'phone',
            'image', 'password'
        )


# Сериализатор для создания токена
class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user:  # and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


# Сериализатор для получения refresh токена
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        data.update({'custom_field': 'custom_data'})
        return data
