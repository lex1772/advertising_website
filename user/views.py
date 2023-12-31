import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import django_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from user.serializers import CustomTokenRefreshSerializer


# Класс для drf-yasg, который переименовывает operation_id
class OperationID(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys):
        operation_id = super(OperationID, self).get_operation_id(operation_keys)
        if operation_id == "api_refresh_create":
            return "Обновить токен"
        return "Получить токен"


# Отображение пользователя
class ActivateUserEmail(APIView):
    """Отображение для отправки ссылки на активацию пользователя через email"""

    @swagger_auto_schema(operation_id="Отправить сообщение на почту пользователя с ссылкой на активацию ")
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        message = result.text
        return Response(message)


@swagger_auto_schema(operation_id="Сбросить пароль пользователя")
def reset_user_password(request, uid, token):
    """Отображение для сброса пароля"""
    if request.POST:
        password = request.POST.get('password1')
        payload = {'uid': uid, 'token': token, 'new_password': password}

        url = '{0}://{1}{2}'.format(
            django_settings.PROTOCOL,
            django_settings.DOMAIN,
            reverse('password_reset_confirm')
        )

        response = requests.post(url, data=payload)
        if response.status_code == 204:
            messages.success(
                request,
                'Your password has been reset successfully!'
            )
            return redirect('home')
        else:
            return Response(response.json())
    else:
        return render(request, 'templates/reset_password.html')


class CustomTokenRefreshView(TokenRefreshView):
    """Отображение для кастомного урла рефреш токена"""
    serializer_class = CustomTokenRefreshSerializer
    swagger_schema = OperationID


class AccessToken(TokenObtainPairSerializer):
    """Отображение для кастомного
     урла аксесс токена, возвращает только аксесс токен"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_name'] = self.user.username
        return data['access']


class AccessTokenView(TokenObtainPairView):
    serializer_class = AccessToken
    swagger_schema = OperationID
