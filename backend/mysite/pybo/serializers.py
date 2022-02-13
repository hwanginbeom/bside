# backend/post/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'name',
            'nickname',
            'provider',
        )
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    nickname = models.CharField(max_length=200, null=True)
    provider = models.CharField(max_length=200, null=True)
    last_login = models.DateTimeField(null=True)
    img = models.CharField(max_length=500, null=True)

class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = (
            'email',
            'meet_id',
            'meet_title',
            'meet_date',
            'status',
            'participants',
            'goal',
            'last_time',
        )


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = (
            'meet_id',
            'agenda_id',
            'agenda_title',
            'discussion',
            'decisions',
            'setting_time',
            'progress_time',
        )


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = (
            'agenda_id',
            'action_id',
            'action_title',
            'person',
            'dead_line',
        )


# 유저 db저장
class UsersaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email', 'name', 'img', 'provider']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            provider=validated_data['provider'],
            img=validated_data['img'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserchkSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    nickname = serializers.CharField(max_length=200, allow_null=True, required=False)

    def validate(self, data):
        email = data.get('email')
        if data.get('nickname'):
            nickname = data.get('nickname')
        else:
            nickname = 'None'
        user = authenticate(email=email)
        if user is None:
            return {'email': 'None', 'nickname': nickname}







# 유저 로그인 진행
User_auth = get_user_model()

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserloginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)
    name = serializers.CharField(max_length=200)
    nickname = serializers.CharField(max_length=200)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        name = data.get('name', None)
        nickname = data.get('nickname', None)
        user = authenticate(email=email, password=password, name=name, nickname=nickname)

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )

        return {'token': token}

