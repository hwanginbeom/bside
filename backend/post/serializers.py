# backend/post/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
# 로그인
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'nickname',
        )


class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = (
            'user_id',
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


#장고 유저모델
auth_user = get_user_model()

#유저 db저장
class UsersaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email', 'username', 'img', 'provider']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            provider=validated_data['provider'],
            img=validated_data['img'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

#유저 체크
class UserchkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            return{
                'email': 'None'
            }
        return {'email': user.email}


#유저 로그인 진행
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserloginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )

        return {'email': user.email, 'token': token}


